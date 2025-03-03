import pytest
from backend.diarization import diarize_speakers

def test_diarize_speakers():
    test_audio_file = "tests/test_audio.wav"
    result = diarize_speakers(test_audio_file)
    assert isinstance(result, str)
    assert "Speaker 1" in result or "Speaker 2" in result
