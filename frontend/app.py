# Import necessary libraries
import streamlit as st
import requests

# Function to upload and analyze audio files
def upload_audio():
    # Set the title of the Streamlit web application
    st.title("Conversation Voice Analyzer")
    
    # Create an audio file uploader
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    
    # If a file is uploaded, display the audio player
    if uploaded_file:
        st.audio(uploaded_file, format='audio/wav')
        
        # Button to trigger speech analysis
        if st.button("Analyze Speech"):
            # Send the uploaded file to the backend for processing
            files = {"audio": uploaded_file}
            response = requests.post("http://localhost:8000/transcribe/", files=files)
            result = response.json()
            
            # Display the transcription result
            st.write("### Transcription")
            st.text(result["transcript"])
            
            # Display the speaker identification result
            st.write("### Speakers Identified")
            st.text(result["speakers"])

# Run the Streamlit app
upload_audio()