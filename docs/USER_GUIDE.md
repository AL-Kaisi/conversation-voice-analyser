# User Guide - Conversation Voice Analyser

## Quick Start

```mermaid
graph LR
    A[Open Browser] --> B[Go to localhost]
    B --> C[Allow Microphone Access]
    C --> D[Start Recording]
    D --> E[Speak]
    E --> F[Stop Recording]
    F --> G[View Results]
```

## Interface Overview

```mermaid
graph TD
    subgraph "Main Interface"
        A[Header: Conversation Voice Analyser]
        B[Language Selector]
        C[Recording Button]
        D[Transcription Display]
        E[Speaker Breakdown]
        F[Recording History List]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
```

## Recording Process

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Recording: Click Start
    Recording --> Processing: Click Stop
    Processing --> DisplayResults: Complete
    DisplayResults --> Ready: New Recording
    
    state Recording {
        [*] --> Capturing
        Capturing --> Capturing: Audio Stream
    }
    
    state Processing {
        [*] --> Transcribing
        Transcribing --> DetectingSpeakers
        DetectingSpeakers --> SavingToDatabase
    }
    
    state DisplayResults {
        [*] --> ShowTranscript
        ShowTranscript --> ShowSpeakers
        ShowSpeakers --> ShowDuration
    }
```

## Language Selection Flow

```mermaid
flowchart TD
    A[Language Dropdown] --> B{Selection}
    B -->|Auto-detect| C[System Detects Language]
    B -->|Manual| D[User Selects Language]
    C --> E[Process with Detection]
    D --> F[Process with Selected Language]
    E --> G[Display Results with Language Tag]
    F --> G
```

## Recording Management

```mermaid
graph TD
    subgraph "Recording Card"
        A[Recording Title]
        B[Language Badge]
        C[Duration Info]
        D[Speaker Count]
        E[Transcript Preview]
        F[Action Buttons]
    end
    
    F --> G[Play Recording]
    F --> H[View Details]
    F --> I[Delete Recording]
    
    H --> J[Full Transcript Modal]
    J --> K[Speaker Timeline]
    J --> L[Complete Text]
```

## Data Storage

```mermaid
graph LR
    A[Audio Recording] --> B[Conversion to WAV]
    B --> C[Speech Recognition]
    C --> D[Speaker Detection]
    D --> E{Save to Database}
    E --> F[Audio Blob]
    E --> G[Transcript Text]
    E --> H[Speaker Segments]
    E --> I[Metadata]
```

## Feature Highlights

### Multi-Language Support
```mermaid
pie title Supported Languages
    "English" : 2
    "Spanish" : 1
    "French" : 1
    "German" : 1
    "Italian" : 1
    "Portuguese" : 2
    "Russian" : 1
    "Japanese" : 1
    "Korean" : 1
    "Chinese" : 1
    "Arabic" : 1
    "Hindi" : 1
```

### Speaker Identification
```mermaid
gantt
    title Speaker Timeline Example
    dateFormat mm:ss
    section Recording
    Speaker 1: active, 00:00, 00:15
    Speaker 2: active, 00:15, 00:30
    Speaker 1: active, 00:30, 00:45
    Speaker 2: active, 00:45, 01:00
```

## Troubleshooting Steps

```mermaid
flowchart TD
    A[Issue?] --> B{Type}
    B -->|No Audio| C[Check Microphone]
    B -->|No Transcript| D[Check Language Setting]
    B -->|App Error| E[Check Browser Console]
    
    C --> F[Browser Settings]
    C --> G[System Permissions]
    
    D --> H[Try Auto-detect]
    D --> I[Select Different Language]
    
    E --> J[Clear Cache]
    E --> K[Restart Application]
```