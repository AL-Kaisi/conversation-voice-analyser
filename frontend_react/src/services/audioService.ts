export const startRecording = async (): Promise<MediaRecorder> => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mediaRecorder = new MediaRecorder(stream);
  return mediaRecorder;
};

export const stopRecording = (mediaRecorder: MediaRecorder) => {
  mediaRecorder.stop();
  mediaRecorder.stream.getTracks().forEach(track => track.stop());
};

export const sendAudioChunk = async (audioBlob: Blob): Promise<Response> => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'audio_chunk.wav');
  
  return fetch('/api/transcribe_stream/', {
    method: 'POST',
    body: formData,
  });
};