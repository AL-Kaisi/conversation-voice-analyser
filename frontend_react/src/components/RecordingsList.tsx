import React, { useState, useEffect } from 'react';
import './RecordingsList.css';

interface Recording {
  id: number;
  filename: string;
  transcript: string;
  language: string;
  speakers: string;
  duration: number;
  created_at: string;
}

interface Speaker {
  speaker: string;
  start: number;
  end: number;
}

const RecordingsList: React.FC = () => {
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRecording, setSelectedRecording] = useState<Recording | null>(null);

  useEffect(() => {
    fetchRecordings();
  }, []);

  const fetchRecordings = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/recordings/');
      if (!response.ok) throw new Error('Failed to fetch recordings');
      const data = await response.json();
      setRecordings(data);
    } catch (err) {
      setError('Failed to load recordings');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const playRecording = async (recordingId: number) => {
    const audioUrl = `/api/recordings/${recordingId}/audio`;
    const audio = new Audio(audioUrl);
    audio.play();
  };

  const deleteRecording = async (recordingId: number) => {
    if (!window.confirm('Are you sure you want to delete this recording?')) return;
    
    try {
      const response = await fetch(`/api/recordings/${recordingId}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Failed to delete recording');
      
      await fetchRecordings(); // Refresh the list
    } catch (err) {
      alert('Failed to delete recording');
      console.error(err);
    }
  };

  const formatDuration = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const parseSpeakers = (speakersJson: string): Speaker[] => {
    try {
      return JSON.parse(speakersJson);
    } catch {
      return [];
    }
  };

  if (loading) return <div className="loading">Loading recordings...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="recordings-list">
      <h2>Recording History</h2>
      
      {recordings.length === 0 ? (
        <p className="no-recordings">No recordings yet. Start recording to see them here!</p>
      ) : (
        <div className="recordings-grid">
          {recordings.map(recording => {
            const speakers = parseSpeakers(recording.speakers);
            return (
              <div key={recording.id} className="recording-card">
                <div className="recording-header">
                  <h3>{recording.filename}</h3>
                  <span className="language-badge">{recording.language.toUpperCase()}</span>
                </div>
                
                <div className="recording-info">
                  <div className="info-item">
                    <span className="label">Duration:</span>
                    <span>{formatDuration(recording.duration)}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Speakers:</span>
                    <span>{speakers.length} detected</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Date:</span>
                    <span>{new Date(recording.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                
                <div className="transcript-preview">
                  {recording.transcript.substring(0, 150)}
                  {recording.transcript.length > 150 && '...'}
                </div>
                
                <div className="recording-actions">
                  <button 
                    onClick={() => playRecording(recording.id)}
                    className="btn btn-sm btn-primary"
                  >
                    Play
                  </button>
                  <button 
                    onClick={() => setSelectedRecording(recording)}
                    className="btn btn-sm btn-secondary"
                  >
                    Details
                  </button>
                  <button 
                    onClick={() => deleteRecording(recording.id)}
                    className="btn btn-sm btn-danger"
                  >
                    Delete
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
      
      {selectedRecording && (
        <div className="modal-overlay" onClick={() => setSelectedRecording(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>{selectedRecording.filename}</h3>
            <div className="modal-details">
              <h4>Full Transcript:</h4>
              <p className="full-transcript">{selectedRecording.transcript}</p>
              
              <h4>Speaker Breakdown:</h4>
              <div className="speakers-list">
                {parseSpeakers(selectedRecording.speakers).map((speaker, index) => (
                  <div key={index} className="speaker-item">
                    <span className="speaker-name">{speaker.speaker}</span>
                    <span className="speaker-time">
                      {formatDuration(speaker.start)} - {formatDuration(speaker.end)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            <button 
              onClick={() => setSelectedRecording(null)}
              className="btn btn-secondary"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecordingsList;