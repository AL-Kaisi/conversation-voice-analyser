import React, { useState } from 'react';
import AudioRecorder from './components/AudioRecorder';
import RecordingsList from './components/RecordingsList';
import './App.css';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  
  const handleRecordingComplete = () => {
    // Refresh the recordings list
    setRefreshKey(prev => prev + 1);
  };
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>Conversation Voice Analyzer</h1>
      </header>
      <main>
        <AudioRecorder onRecordingComplete={handleRecordingComplete} />
        <RecordingsList key={refreshKey} />
      </main>
    </div>
  );
}

export default App;