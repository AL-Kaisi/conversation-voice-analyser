# Conversation Voice Analyser

## Overview
The **Conversation Voice Analyzer** is an end-to-end application that records, transcribes, and analyzes speech while distinguishing between multiple speakers. It integrates with **Azure Speech-to-Text** for transcription, **Azure SQL Database** for data storage, and **Terraform** for infrastructure automation.

## Features
- **Speech Recording:** Capture and save audio files.
- **Speech Recognition:** Convert speech to text using Azure Speech-to-Text.
- **Speaker Diarization:** Identify and differentiate multiple speakers.
- **Database Storage:** Store transcriptions in Azure SQL Database.
- **Web Interface:** Streamlit-based frontend for file uploads and analysis.
- **Infrastructure as Code:** Deploy cloud infrastructure with Terraform.
- **Containerization:** Run the application using Docker.

## Architecture
The system consists of:
- **Frontend:** Streamlit UI for uploading audio and displaying results.
- **Backend:** FastAPI-based API for handling speech processing.
- **Database:** Azure SQL Database for storing transcriptions.
- **Cloud Deployment:** Azure App Services for hosting.
- **Infrastructure:** Terraform for provisioning Azure resources.

## Project Structure
```plaintext
conversation-voice-analyzer/
│── backend/                    # FastAPI backend for processing audio
│   ├── main.py                  # API entry point
│   ├── audio_recorder.py        # Audio recording logic
│   ├── speech_processing.py     # Speech recognition using Azure
│   ├── diarization.py           # Speaker separation using Azure
│   ├── database.py              # Database connection
│   ├── requirements.txt         # Backend dependencies
│   ├── Dockerfile               # Backend Docker configuration
│
│── frontend/                   # Streamlit web interface
│   ├── app.py                   # Main UI logic
│   ├── requirements.txt         # Frontend dependencies
│   ├── Dockerfile               # Frontend Docker configuration
│
│── terraform/                   # Terraform for infrastructure automation
│   ├── main.tf                   # Azure resource definitions
│
│── .github/                     # CI/CD pipelines
│   ├── workflows/
│       ├── deployment.yml        # GitHub Actions for deployment
│
│── .gitignore                   # Ignore unnecessary files
│── README.md                    # Project documentation
```

## Prerequisites
Before running the project, install:
- **Python 3.9+**
- **Terraform**
- **Azure CLI**
- **Docker**
- **FastAPI & Streamlit** (see `requirements.txt`)

## Running Locally
### 1. Set Up a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```sh
cd backend
pip install -r requirements.txt
cd ../frontend
pip install -r requirements.txt
```

### 3. Run the Backend and Frontend
#### Start Backend (FastAPI)
```sh
cd backend
uvicorn main:app --reload
```

#### Start Frontend (Streamlit)
```sh
cd frontend
streamlit run app.py
```

## Running with Docker
### 1. Build and Run Containers
```sh
cd terraform
terraform init
terraform apply -auto-approve
```

```sh
docker-compose up --build
```

## Azure Deployment
### 1. Login to Azure and Create a Resource Group
```sh
az login
az group create --name voice-analyzer-rg --location "East US"
```

### 2. Deploy with Terraform
```sh
cd terraform
terraform init
terraform apply -auto-approve
```

### 3. Push Docker Images to Azure Container Registry
```sh
docker tag backend myregistry.azurecr.io/backend
docker tag frontend myregistry.azurecr.io/frontend
docker push myregistry.azurecr.io/backend
docker push myregistry.azurecr.io/frontend
```

### 4. Deploy Services to Azure
```sh
az webapp create --resource-group voice-analyzer-rg --plan voice-analyzer-plan \
  --name voice-analyzer-api --deployment-container-image-name myregistry.azurecr.io/backend

az webapp create --resource-group voice-analyzer-rg --plan voice-analyzer-plan \
  --name voice-analyzer-ui --deployment-container-image-name myregistry.azurecr.io/frontend
```

## Next Steps
- Implement **real-time streaming transcription**
- Enhance **UI visualization** for speaker differentiation
- Optimize **performance for large-scale audio files**

## Contributing
Pull requests are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Commit changes and push.
4. Submit a pull request.

## License
MIT License

