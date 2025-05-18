from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import io
import wave
import numpy as np
from speech_processing import transcribe_and_store, transcribe_stream
import asyncio
import os
import shutil
import tempfile
from pydub import AudioSegment
import json
from database import SessionLocal, Recording
from datetime import datetime

app = FastAPI()

# Add CORS middleware to allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe/")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = "auto"
):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        # Save uploaded file
        contents = await audio.read()
        tmp.write(contents)
        tmp_path = tmp.name
    
    try:
        # Try to convert to WAV if needed
        try:
            # Try to open with pydub
            audio_segment = AudioSegment.from_file(tmp_path)
            wav_path = tmp_path.replace(os.path.splitext(tmp_path)[1], ".wav")
            audio_segment.export(wav_path, format="wav")
            
            # Use the WAV file for transcription
            result = transcribe_and_store(wav_path, audio.filename, language)
            
            # Clean up
            if wav_path != tmp_path:
                os.remove(wav_path)
        except:
            # If pydub fails, try direct transcription
            result = transcribe_and_store(tmp_path, audio.filename, language)
        
        return result
    finally:
        # Clean up temporary file
        os.remove(tmp_path)

@app.get("/recordings/")
async def list_recordings(
    limit: int = 10,
    offset: int = 0
):
    db = SessionLocal()
    try:
        recordings = db.query(Recording).order_by(Recording.created_at.desc()).offset(offset).limit(limit).all()
        return [recording.to_dict() for recording in recordings]
    finally:
        db.close()

@app.get("/recordings/{recording_id}")
async def get_recording(recording_id: int):
    db = SessionLocal()
    try:
        recording = db.query(Recording).filter(Recording.id == recording_id).first()
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        return recording.to_dict()
    finally:
        db.close()

@app.get("/recordings/{recording_id}/audio")
async def get_recording_audio(recording_id: int):
    db = SessionLocal()
    try:
        recording = db.query(Recording).filter(Recording.id == recording_id).first()
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        # Return audio data as a downloadable file
        return StreamingResponse(
            io.BytesIO(recording.audio_data),
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; filename={recording.filename}"
            }
        )
    finally:
        db.close()

@app.delete("/recordings/{recording_id}")
async def delete_recording(recording_id: int):
    db = SessionLocal()
    try:
        recording = db.query(Recording).filter(Recording.id == recording_id).first()
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        db.delete(recording)
        db.commit()
        return {"message": "Recording deleted successfully"}
    finally:
        db.close()

@app.post("/transcribe_stream/")
async def transcribe_stream_endpoint(audio: UploadFile = File(...)):
    # Read the audio chunk
    audio_data = await audio.read()
    
    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        with wave.open(tmp.name, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(44100)
            
            # Convert bytes to numpy array
            if isinstance(audio_data, bytes) and len(audio_data) > 0:
                try:
                    audio_array = np.frombuffer(audio_data, dtype=np.int16)
                    wav_file.writeframes(audio_array.tobytes())
                except:
                    # If conversion fails, write raw data
                    wav_file.writeframes(audio_data)
            else:
                wav_file.writeframes(audio_data)
        
        tmp_path = tmp.name
    
    try:
        # Use speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio_chunk = recognizer.record(source)
            
            try:
                transcript = recognizer.recognize_google(audio_chunk)
            except sr.UnknownValueError:
                transcript = ""
            except sr.RequestError as e:
                transcript = f"Error: {e}"
        
        # Return as streaming response
        async def generate():
            yield transcript
        
        return StreamingResponse(generate(), media_type="text/plain")
    finally:
        # Clean up
        os.remove(tmp_path)

@app.get("/")
def read_root():
    return {"message": "Voice Analyzer API - Local Speech Recognition"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}