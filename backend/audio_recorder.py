# Import necessary libraries
import sounddevice as sd
import wave

# Function to record audio and save to file
def record_audio(filename, duration=10, samplerate=44100):
    print(f"Recording audio for {duration} seconds...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()
    
    # Save the recorded audio to a file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    print(f"Audio saved to {filename}")