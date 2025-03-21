"""
main.py - FastAPI Backend for the AI Audio Diary

This file defines the FastAPI backend, handling:
- Audio upload
- Speech-to-text conversion
- Emotion detection (using tone + text)
- AI-generated responses based on emotion + text
- Text-to-speech conversion for voice responses
- Storing and retrieving diary entries
"""

from fastapi import FastAPI, UploadFile, File
import speech_to_text
import emotion_analysis
import text_response
import text_to_speech
import database

app = FastAPI()

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    """
    Handles audio file upload.
    - Converts audio to text using speech-to-text module.
    - Detects emotions using tone + text.
    - Generates AI response based on emotion + text.
    - Converts the response into speech.
    - Stores everything in the database.
    """
    audio_text = speech_to_text.convert_audio_to_text(await file.read())  # Convert audio to text
    emotion_results = emotion_analysis.analyze_audio(file.file)  # Analyze tone + text for emotion
    ai_response = text_response.generate_response(audio_text, emotion_results)  # Generate response using both
    speech_output = text_to_speech.convert_text_to_speech(ai_response)  # Convert response to speech
    
    database.store_entry(audio_text, emotion_results, ai_response)  # Save in DB
    
    return {"transcription": audio_text, "emotion": emotion_results, "response": ai_response, "audio_response": speech_output}

@app.get("/diary-entries/")
def get_entries():
    """ Fetches all stored diary entries from the database. """
    return database.get_entries()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
