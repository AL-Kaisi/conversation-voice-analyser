# File: tests/test_diarization.py

import pytest
import azure.cognitiveservices.speech as speechsdk
from backend.diarization import diarize_speakers
from unittest.mock import patch, MagicMock

def test_diarize_speakers():
    test_audio_file = "tests/test_audio.wav"
    
    with patch("azure.cognitiveservices.speech.SpeechConfig") as MockSpeechConfig, \
         patch("azure.cognitiveservices.speech.AudioConfig") as MockAudioConfig, \
         patch("azure.cognitiveservices.speech.transcription.ConversationTranscriber") as MockTranscriber:
        
        mock_transcriber_instance = MockTranscriber.return_value
        mock_result = MagicMock()
        mock_result.text = "Speaker 1: Hello, Speaker 2: Hi there."
        mock_transcriber_instance.transcribe_once.return_value = mock_result
        
        result = diarize_speakers(test_audio_file)
        assert isinstance(result, str)
        assert "Speaker 1" in result or "Speaker 2" in result
