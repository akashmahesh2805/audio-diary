# app.py
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import librosa # type: ignore
import torch # type: ignore
from .model import analyze_audio  # Use relative import

app = FastAPI()

# Endpoint to upload audio file and analyze it
@app.post("/analyze_voice/")
async def analyze_voice(file: UploadFile = File(...)):
    # Save the uploaded file
    with open("temp_audio.wav", "wb") as f:
        f.write(await file.read())
    
    # Analyze the audio file (Returns a dictionary with 'emotion' and 'sentiment')
    result = analyze_audio("temp_audio.wav")
    return result
