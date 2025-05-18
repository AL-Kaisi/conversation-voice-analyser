# Use Python 3.9 as the base image
FROM python:3.9

# Install audio processing dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    flac \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI backend server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]