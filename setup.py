from setuptools import setup, find_packages

setup(
name="conversation_voice_analyzer",
version="1.0.0",
author="Your Name",
author_email="your.email@example.com",
description="A Python-based voice analyzer application using Azure Speech-to-Text and Terraform",
long_description=open("README.md").read(),
long_description_content_type="text/markdown",
url="https://github.com/yourusername/conversation-voice-analyzer",
packages=find_packages(),
install_requires=[
"fastapi",
"uvicorn",
"azure-cognitiveservices-speech",
"python-dotenv",
"sounddevice",
"numpy",
"wave",
"sqlalchemy",
"psycopg2-binary",
"requests",
"pyodbc",
"streamlit"
],
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
python_requires='>=3.9',
entry_points={
"console_scripts": [
"start-backend=backend.main:app",
"start-frontend=frontend.app:upload_audio",
],
},
)

