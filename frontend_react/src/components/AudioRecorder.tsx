import React, { useState, useRef, useCallback } from 'react';
import './AudioRecorder.css';

interface AudioRecorderProps {
  onRecordingComplete?: () => void;
}

const AudioRecorder: React.FC<AudioRecorderProps> = ({ onRecordingComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcribedText, setTranscribedText] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState('auto');
  const [processingResults, setProcessingResults] = useState<any>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const supportedLanguages = [
    { code: 'auto', name: 'Auto-detect' },
    { code: 'en-US', name: 'English (US)' },
    { code: 'en-GB', name: 'English (UK)' },
    { code: 'es-ES', name: 'Spanish' },
    { code: 'fr-FR', name: 'French' },
    { code: 'de-DE', name: 'German' },
    { code: 'it-IT', name: 'Italian' },
    { code: 'pt-BR', name: 'Portuguese (Brazil)' },
    { code: 'pt-PT', name: 'Portuguese (Portugal)' },
    { code: 'ru-RU', name: 'Russian' },
    { code: 'ja-JP', name: 'Japanese' },
    { code: 'ko-KR', name: 'Korean' },
    { code: 'zh-CN', name: 'Chinese (Simplified)' },
    { code: 'ar-SA', name: 'Arabic' },
    { code: 'hi-IN', name: 'Hindi' },
  ];

  const handleStartRecording = useCallback(async () => {
    try {
      setError(null);
      setTranscribedText('');
      setProcessingResults(null);
      chunksRef.current = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Check for best supported format
      let mimeType = 'audio/webm';
      if (MediaRecorder.isTypeSupported('audio/webm')) {
        mimeType = 'audio/webm';
      } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
        mimeType = 'audio/mp4';
      } else if (MediaRecorder.isTypeSupported('audio/wav')) {
        mimeType = 'audio/wav';
      }
      
      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: mimeType });
        await sendAudioForTranscription(audioBlob);
      };
      
      mediaRecorder.start();
      setIsRecording(true);
      
    } catch (err) {
      setError('Failed to access microphone. Please check permissions.');
      console.error(err);
    }
  }, [selectedLanguage]);
  
  const handleStopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  }, []);
  
  const sendAudioForTranscription = async (audioBlob: Blob) => {
    try {
      const formData = new FormData();
      // Send with correct filename extension based on type
      let filename = 'recording';
      if (audioBlob.type.includes('webm')) {
        filename += '.webm';
      } else if (audioBlob.type.includes('mp4')) {
        filename += '.mp4';
      } else {
        filename += '.wav';
      }
      
      formData.append('audio', audioBlob, filename);
      
      const response = await fetch(`/api/transcribe/?language=${selectedLanguage}`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to transcribe audio: ${errorText}`);
      }
      
      const data = await response.json();
      setTranscribedText(data.transcript);
      setProcessingResults(data);
      
      if (!data.transcript || data.transcript.startsWith('Error')) {
        setError('Failed to transcribe audio. Please speak clearly and try again.');
      }
      
      // Notify parent component
      if (onRecordingComplete) {
        onRecordingComplete();
      }
    } catch (err) {
      console.error('Error transcribing audio:', err);
      setError('Failed to transcribe audio. Please try again.');
    }
  };
  
  const formatDuration = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };
  
  return (
    <div className="audio-recorder">
      <h2>Voice Transcription</h2>
      
      <div className="language-selector">
        <label htmlFor="language-select">Language:</label>
        <select 
          id="language-select"
          value={selectedLanguage} 
          onChange={(e) => setSelectedLanguage(e.target.value)}
          disabled={isRecording}
        >
          {supportedLanguages.map(lang => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
      </div>
      
      <div className="controls">
        {!isRecording ? (
          <button onClick={handleStartRecording} className="btn btn-primary">
            Start Recording
          </button>
        ) : (
          <button onClick={handleStopRecording} className="btn btn-danger">
            Stop Recording
          </button>
        )}
      </div>
      
      {error && <div className="error">{error}</div>}
      
      <div className="transcription">
        <h3>Transcribed Text:</h3>
        <div className="transcription-text">
          {transcribedText || 'Click "Start Recording" and speak clearly into your microphone...'}
        </div>
      </div>
      
      {processingResults && (
        <div className="processing-results">
          <div className="result-item">
            <span className="label">Detected Language:</span>
            <span>{processingResults.language}</span>
          </div>
          <div className="result-item">
            <span className="label">Duration:</span>
            <span>{formatDuration(processingResults.duration)}</span>
          </div>
          <div className="result-item">
            <span className="label">Speakers Detected:</span>
            <span>{processingResults.speakers?.length || 0}</span>
          </div>
        </div>
      )}
      
      {processingResults && processingResults.speakers && (
        <div className="speakers-breakdown">
          <h4>Speaker Breakdown:</h4>
          {processingResults.speakers.map((speaker: any, index: number) => (
            <div key={index} className="speaker-info">
              <span className="speaker-label">{speaker.speaker}:</span>
              <span className="speaker-time">
                {formatDuration(speaker.start)} - {formatDuration(speaker.end)}
              </span>
            </div>
          ))}
        </div>
      )}
      
      <div className="info">
        <p><small>Using local speech recognition with Google Web Speech API</small></p>
      </div>
    </div>
  );
};

export default AudioRecorder;