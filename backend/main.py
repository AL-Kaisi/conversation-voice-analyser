# Import necessary libraries
from fastapi import FastAPI, UploadFile, File, Depends
import shutil
from sqlalchemy.orm import Session
from database import SessionLocal, Transcription
from speech_processing import transcribe_audio
from diarization import diarize_speakers

# Initialize FastAPI application
app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define API endpoint for transcription
@app.post("/transcribe/")
async def transcribe(audio: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save uploaded audio file to a local directory
    file_path = f"data/recordings/{audio.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    
    # Process the audio file with Azure Speech-to-Text and diarization
    transcript = transcribe_audio(file_path)
    speakers = diarize_speakers(file_path)
    
    # Store result in Azure SQL Database
    db_transcription = Transcription(filename=audio.filename, transcript=transcript, speakers=speakers)
    db.add(db_transcription)
    db.commit()
    db.refresh(db_transcription)
    
    # Return transcription and speaker identification results
    return {"transcript": transcript, "speakers": speakers}

# Start the FastAPI server when running the script directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)