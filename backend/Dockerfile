# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI backend server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]