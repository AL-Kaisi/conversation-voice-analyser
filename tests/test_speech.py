import pytest
import azure.cognitiveservices.speech as speechsdk
from backend.speech_processing import transcribe_audio
from unittest.mock import patch, MagicMock

def test_transcribe_audio():
    test_audio_file = "tests/test_audio.wav"
    
    with patch("azure.cognitiveservices.speech.SpeechConfig") as MockSpeechConfig, \
         patch("azure.cognitiveservices.speech.AudioConfig") as MockAudioConfig, \
         patch("azure.cognitiveservices.speech.SpeechRecognizer") as MockRecognizer:
        
        mock_recognizer_instance = MockRecognizer.return_value
        mock_result = MagicMock()
        mock_result.text = "Hello, this is a test."
        mock_result.reason = speechsdk.ResultReason.RecognizedSpeech
        mock_recognizer_instance.recognize_once.return_value = mock_result
        
        result = transcribe_audio(test_audio_file)
        assert isinstance(result, str)
        assert len(result) > 0
