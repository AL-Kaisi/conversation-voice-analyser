# Conversation Voice Analyser

## Overview
The **Conversation Voice Analyser** is a comprehensive speech analysis application that records, transcribes, and analyses conversations whilst identifying different speakers. Built with modern web technologies, it operates completely locally without requiring cloud services.

## Key Features
- **Recording Management:** Save, playback, and manage audio recordings
- **Speaker Diarisation:** Automatically identify and separate different speakers
- **Multi-Language Support:** Transcribe in 15+ languages with auto-detection
- **Real-Time Processing:** Live transcription with speaker identification
- **Local Processing:** All data processed locally for privacy
- **Modern UI:** Responsive React interface with TypeScript

## Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │
│  React Frontend     │────▶│  FastAPI Backend    │
│  (TypeScript)       │     │  (Python)           │
│                     │     │                     │
│  • Audio Recording  │     │  • Speech Recognition│
│  • UI Components    │     │  • Speaker Detection │
│  • Recording List   │     │  • Database Storage  │
│                     │     │                     │
└─────────────────────┘     └──────────┬──────────┘
                                      │
                                      ▼
                            ┌─────────────────────┐
                            │                     │
                            │  SQLite Database    │
                            │                     │
                            │  • Recordings       │
                            │  • Transcripts      │
                            │  • Speaker Data     │
                            │                     │
                            └─────────────────────┘
```

## Processing Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │     │              │
│  Microphone  │────▶│ Audio Capture│────▶│ Speech-to-   │────▶│  Speaker     │
│   Input      │     │ (WebRTC)     │     │    Text      │     │  Diarisation │
│              │     │              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────┬───────┘
                                                                      │
                                                                      ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │     │              │
│   Display    │◀────│   React UI   │◀────│   Database   │◀────│   Storage    │
│   Results    │     │   Update     │     │    Save      │     │  & Analysis  │
│              │     │              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

## Project Structure
```
conversation-voice-analyser/
├── backend/                     # FastAPI backend
│   ├── main.py                 # API endpoints
│   ├── speech_processing.py    # Speech recognition & diarisation
│   ├── database.py            # Database models
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Backend container config
│
├── frontend_react/            # React frontend
│   ├── src/
│   │   ├── App.tsx           # Main app component
│   │   ├── components/       # React components
│   │   │   ├── AudioRecorder.tsx
│   │   │   └── RecordingsList.tsx
│   │   └── services/         # API services
│   ├── package.json          # Node dependencies
│   └── Dockerfile            # Frontend container config
│
├── docker-compose.yml         # Container orchestration
└── README.md                 # Documentation
```

## Technologies Used

### Frontend
- **React** with TypeScript
- **Vite** for build tooling
- **Web Audio API** for recording
- **Modern CSS** for styling

### Backend
- **FastAPI** for REST API
- **SpeechRecognition** library
- **WebRTC VAD** for speaker detection
- **PyDub** for audio processing
- **SQLAlchemy** for database ORM

### Infrastructure
- **Docker** for containerisation
- **Nginx** for frontend serving
- **SQLite** for local storage

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

### Running with Docker
```bash
# Clone the repository
git clone <repository-url>
cd conversation-voice-analyser

# Start the application
docker-compose up --build

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
```

### Local Development
```bash
# Backend setup
cd backend
python -m venv venv
source venv/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup (in new terminal)
cd frontend_react
npm install
npm run dev
```

## Usage Guide

### 1. Recording Audio
- Click "Start Recording" button
- Speak into your microphone
- Click "Stop Recording" when finished
- View real-time transcription

### 2. Language Selection
- Choose from 15+ supported languages
- Use "Auto-detect" for automatic language detection
- Language affects transcription accuracy

### 3. Viewing Recording History
- All recordings appear below the recorder
- Click "Play" to listen to recordings
- Click "Details" for full transcript and speaker info
- Click "Delete" to remove recordings

### 4. Speaker Identification
- Automatic detection of multiple speakers
- Shows speaker timestamps
- Displays total speaker count

## Supported Languages
- English (US/UK)
- Spanish
- French
- German
- Italian
- Portuguese (Brazil/Portugal)
- Russian
- Japanese
- Korean
- Chinese (Simplified)
- Arabic
- Hindi

## Privacy & Security
- All processing happens locally
- No cloud services required
- Audio stored in local SQLite database
- No external API calls for sensitive data

## API Endpoints

### Backend API
```
POST   /transcribe/              # Process and save recording
GET    /recordings/              # List all recordings
GET    /recordings/{id}          # Get recording details
GET    /recordings/{id}/audio    # Download audio file
DELETE /recordings/{id}          # Delete recording
```

## Troubleshooting

### Common Issues

1. **Microphone Access Denied**
   - Check browser permissions
   - Ensure HTTPS or localhost
   - Allow microphone access when prompted

2. **Docker Build Fails**
   ```bash
   docker system prune -f
   docker-compose build --no-cache
   ```

3. **Audio Not Recording**
   - Check microphone is connected
   - Test in browser settings
   - Restart Docker containers

## Future Enhancements
- Real-time streaming transcription
- Advanced speaker recognition
- Export transcripts to various formats
- Enhanced visualisation of conversations
- Cloud deployment options
- Mobile responsive improvements

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Licence
MIT Licence - See LICENCE file for details

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - System design and technical details
- [User Guide](docs/USER_GUIDE.md) - Detailed usage instructions with visuals
- [Feature Documentation](docs/FEATURES.md) - Complete feature set and roadmap

## Acknowledgements
- Google Web Speech API for transcription
- WebRTC VAD for voice activity detection
- FastAPI and React communities

---

<div align="center">
  <p>Built with care for better conversation analysis</p>
  <p>
    <a href="https://github.com/yourusername/conversation-voice-analyser">GitHub</a> •
    <a href="docs/USER_GUIDE.md">User Guide</a> •
    <a href="docs/ARCHITECTURE.md">Architecture</a> •
    <a href="#contributing">Contribute</a>
  </p>
</div>