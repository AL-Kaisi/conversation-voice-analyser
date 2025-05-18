# Architecture Documentation

## System Architecture

```mermaid
graph TB
    subgraph "Frontend (React)"
        A[AudioRecorder Component]
        B[RecordingsList Component]
        C[API Service Layer]
    end
    
    subgraph "Backend (FastAPI)"
        D[API Endpoints]
        E[Speech Processing]
        F[Speaker Diarisation]
        G[Database Handler]
    end
    
    subgraph "Storage"
        H[(SQLite Database)]
    end
    
    subgraph "External Services"
        I[Google Speech API]
    end
    
    A --> C
    B --> C
    C -->|HTTP/REST| D
    D --> E
    D --> G
    E --> F
    E -->|Speech Recognition| I
    G --> H
    
    style A fill:#61dafb,stroke:#333,stroke-width:2px
    style B fill:#61dafb,stroke:#333,stroke-width:2px
    style D fill:#009485,stroke:#333,stroke-width:2px
    style H fill:#336791,stroke:#333,stroke-width:2px
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant S as Speech API
    participant D as Database
    
    U->>F: Click "Start Recording"
    F->>F: Capture Audio Stream
    U->>F: Click "Stop Recording"
    F->>B: POST /transcribe/
    B->>S: Send Audio for Recognition
    S->>B: Return Transcript
    B->>B: Detect Speakers (VAD)
    B->>D: Save Recording Data
    D->>B: Confirm Save
    B->>F: Return Results
    F->>U: Display Transcript & Speakers
```

## Component Architecture

```mermaid
graph LR
    subgraph "Frontend Components"
        A[App.tsx]
        B[AudioRecorder.tsx]
        C[RecordingsList.tsx]
        D[audioService.ts]
    end
    
    subgraph "Backend Modules"
        E[main.py]
        F[speech_processing.py]
        G[database.py]
    end
    
    A --> B
    A --> C
    B --> D
    C --> D
    D --> E
    E --> F
    E --> G
    F --> G
```

## Database Schema

```mermaid
erDiagram
    RECORDINGS {
        int id PK
        string filename
        blob audio_data
        text transcript
        string language
        text speakers
        float duration
        datetime created_at
    }
```

## Speaker Detection Flow

```mermaid
flowchart TD
    A[Audio Input] --> B[Convert to Mono 16kHz]
    B --> C[Split into Frames]
    C --> D{Voice Activity Detection}
    D -->|Speech| E[Add to Current Speaker]
    D -->|Silence| F{Silence > Threshold?}
    F -->|Yes| G[New Speaker Detected]
    F -->|No| H[Continue Current Speaker]
    E --> I[Continue Processing]
    G --> I
    H --> I
    I --> J{End of Audio?}
    J -->|No| C
    J -->|Yes| K[Return Speaker Segments]
```

## Deployment Architecture

```mermaid
graph TD
    subgraph "Docker Containers"
        A[Frontend Container<br/>Nginx + React Build]
        B[Backend Container<br/>Python + FastAPI]
    end
    
    subgraph "Network"
        C[Docker Network Bridge]
    end
    
    subgraph "Storage"
        D[SQLite Volume]
    end
    
    subgraph "Host"
        E[Port 80]
        F[Port 8000]
    end
    
    E --> A
    F --> B
    A --> C
    B --> C
    A -.->|Proxy /api| B
    B --> D
    
    style A fill:#e34c26,stroke:#333,stroke-width:2px
    style B fill:#3776ab,stroke:#333,stroke-width:2px
```

## Language Detection Process

```mermaid
flowchart LR
    A[Audio Input] --> B{Language Setting}
    B -->|Auto| C[Try English Recognition]
    B -->|Selected| D[Use Selected Language]
    C --> E{Confidence Score}
    E -->|High| F[Use English]
    E -->|Low| G[Try Other Languages]
    G --> H[Select Best Match]
    D --> I[Process Transcript]
    F --> I
    H --> I
```

## Security & Privacy Flow

```mermaid
graph TD
    A[User Audio] -->|Local Only| B[Browser]
    B -->|HTTPS/Localhost| C[Frontend]
    C -->|Internal Network| D[Backend]
    D -->|No External Calls| E[Local Processing]
    E --> F[SQLite Storage]
    
    style A fill:#ff6b6b,stroke:#333,stroke-width:2px
    style E fill:#51cf66,stroke:#333,stroke-width:2px
    style F fill:#339af0,stroke:#333,stroke-width:2px
```