import pyaudio

# Capture system audio (Windows only)
def record_system_audio(filename="system_audio.wav", duration=10, samplerate=44100, channels=2):
    p = pyaudio.PyAudio()
    
    # Open a recording stream for system audio
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=1024)
    
    print(f"Recording system audio for {duration} seconds...")
    
    frames = []
    for _ in range(int(samplerate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    print(f"Recording complete. Saving to {filename}...")

    # Save the recorded audio to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(samplerate)
        wf.writeframes(b''.join(frames))
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print(f"System audio saved to {filename}")
