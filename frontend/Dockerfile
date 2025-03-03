# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Streamlit web application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]