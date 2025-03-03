# File: backend/speech_processing.py

# Import necessary libraries
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Azure Speech API credentials from environment variables
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")

# Function to transcribe audio using Azure Speech-to-Text
def transcribe_audio(audio_file):
    # Configure Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_input = speechsdk.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
    # Perform speech recognition
    result = speech_recognizer.recognize_once()
    
    # Return the transcribed text if successful, otherwise return an error message
    return result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else "Error processing audio"
