from fastapi import FastAPI, UploadFile
import speech_to_text
import emotion_analysis
import text_response
import text_to_speech
import database

app = FastAPI()

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile):
    audio_text = speech_to_text.convert_audio_to_text(file.file)
    emotion_results = emotion_analysis.analyze_text(audio_text)
    ai_response = text_response.generate_response(emotion_results)
    speech_output = text_to_speech.convert_text_to_speech(ai_response)
    
    database.store_entry(audio_text, emotion_results, ai_response)
    
    return {"transcription": audio_text, "emotion": emotion_results, "response": ai_response, "audio_response": speech_output}

@app.get("/diary-entries/")
def get_entries():
    return database.get_entries()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
