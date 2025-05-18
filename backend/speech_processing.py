import speech_recognition as sr
import os
import json
import wave
import numpy as np
from database import SessionLocal, Recording
from dotenv import load_dotenv
from pydub import AudioSegment
from datetime import datetime
import webrtcvad

# Load environment variables
load_dotenv()

def detect_speakers(audio_path):
    """Simple speaker detection based on voice activity detection and pauses"""
    # Load audio
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    
    # Convert to raw PCM data
    samples = np.array(audio.get_array_of_samples())
    
    # Simple voice activity detection
    vad = webrtcvad.Vad(2)  # Aggressiveness level 2
    frame_duration = 30  # milliseconds
    frame_size = int(16000 * frame_duration / 1000)
    
    speakers = []
    current_speaker = 1
    speech_frames = []
    silence_threshold = 10  # Number of silent frames to consider speaker change
    silence_count = 0
    
    for i in range(0, len(samples), frame_size):
        frame = samples[i:i + frame_size]
        if len(frame) < frame_size:
            frame = np.pad(frame, (0, frame_size - len(frame)))
        
        # Convert to bytes
        frame_bytes = frame.astype(np.int16).tobytes()
        
        try:
            is_speech = vad.is_speech(frame_bytes, 16000)
            
            if is_speech:
                if silence_count > silence_threshold:
                    # New speaker detected
                    if speech_frames:
                        speakers.append({
                            'speaker': f'Speaker {current_speaker}',
                            'start': speech_frames[0] * frame_duration / 1000,
                            'end': speech_frames[-1] * frame_duration / 1000
                        })
                        current_speaker += 1
                        speech_frames = []
                
                speech_frames.append(i // frame_size)
                silence_count = 0
            else:
                silence_count += 1
        except:
            # If VAD fails, assume it's speech
            if speech_frames:
                speech_frames.append(i // frame_size)
    
    # Add last speaker
    if speech_frames:
        speakers.append({
            'speaker': f'Speaker {current_speaker}',
            'start': speech_frames[0] * frame_duration / 1000,
            'end': speech_frames[-1] * frame_duration / 1000
        })
    
    # If no speakers detected, assume single speaker
    if not speakers:
        speakers = [{
            'speaker': 'Speaker 1',
            'start': 0,
            'end': len(audio) / 1000
        }]
    
    return speakers

# Function to perform transcription and save to database
def transcribe_and_store(audio_file, filename, language='auto'):
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    
    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    
    # Detect language if auto
    if language == 'auto':
        # Try to detect language from first few seconds
        try:
            # First try with English
            sample_text = recognizer.recognize_google(audio_data, language='en-US', show_all=True)
            if sample_text and 'alternative' in sample_text:
                # If confidence is low, try other languages
                confidence = sample_text['alternative'][0].get('confidence', 0)
                if confidence < 0.8:
                    # Try Spanish
                    try:
                        sample_text_es = recognizer.recognize_google(audio_data, language='es-ES', show_all=True)
                        if sample_text_es and 'alternative' in sample_text_es:
                            confidence_es = sample_text_es['alternative'][0].get('confidence', 0)
                            if confidence_es > confidence:
                                language = 'es-ES'
                            else:
                                language = 'en-US'
                    except:
                        language = 'en-US'
                else:
                    language = 'en-US'
            else:
                language = 'en-US'
        except:
            language = 'en-US'
    
    # Perform speech recognition with detected/specified language
    try:
        transcript = recognizer.recognize_google(audio_data, language=language)
    except sr.UnknownValueError:
        transcript = "Could not understand the audio"
    except sr.RequestError as e:
        transcript = f"Error processing audio: {e}"
    
    # Get audio duration
    with wave.open(audio_file, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    
    # Detect speakers
    speakers = detect_speakers(audio_file)
    
    # Read audio file data
    with open(audio_file, 'rb') as f:
        audio_data = f.read()
    
    # Store in database
    db = SessionLocal()
    db_recording = Recording(
        filename=filename,
        audio_data=audio_data,
        transcript=transcript,
        language=language.split('-')[0],  # Store just language code
        speakers=json.dumps(speakers),
        duration=duration
    )
    db.add(db_recording)
    db.commit()
    db.refresh(db_recording)
    db.close()
    
    return {
        'transcript': transcript,
        'language': language,
        'speakers': speakers,
        'duration': duration
    }

# Function for streaming transcription
def transcribe_stream(audio_chunk):
    recognizer = sr.Recognizer()
    
    try:
        # Convert audio chunk to recognizable format
        audio_data = sr.AudioData(audio_chunk, 44100, 2)
        
        # Perform recognition
        transcript = recognizer.recognize_google(audio_data)
        return transcript
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"Error: {e}"