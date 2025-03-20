from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import speech_to_text
import emotion_analysis
import text_response
import text_to_speech
import database
import asyncio

# Create a FastAPI instance
app = FastAPI()

# List to store active WebSocket connections (for multi-client support)
active_connections = []


# WebSocket endpoint for real-time audio streaming
@app.websocket("/audio-stream/")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()  # Accept the client connection
    active_connections.append(websocket)  # Add connection to the active list
    
    try:
        while True:
            # Receive audio data in chunks from the client
            audio_chunk = await websocket.receive_bytes()

            # Convert audio to text using the speech-to-text module
            text = await asyncio.to_thread(speech_to_text.process_chunk, audio_chunk)

            # Analyze emotional tone from audio using emotion analysis module
            emotion = await asyncio.to_thread(emotion_analysis.analyze_audio_chunk, audio_chunk)

            # Generate an AI-based response using the extracted text and emotion
            response = await asyncio.to_thread(text_response.generate_response, text, emotion)

            # Convert the generated response to speech using text-to-speech
            speech_output = await asyncio.to_thread(text_to_speech.convert_text_to_speech, response)

            # Store session details in the database (text, emotion, response)
            await asyncio.to_thread(database.store_entry, text, emotion, response)

            # Send the response (text + audio) back to the client over WebSocket
            await websocket.send_json({
                "transcription": text,
                "emotion": emotion,
                "response": response,
                "audio_response": speech_output
            })

    except WebSocketDisconnect:
        # Handle client disconnection
        print("Client disconnected")
        active_connections.remove(websocket)


# Endpoint to retrieve all stored diary entries from the database
@app.get("/diary-entries/")
async def get_entries():
    # Fetch all entries from the database using the `get_entries` function
    entries = await asyncio.to_thread(database.get_entries)
    return {"entries": entries}


# Run the FastAPI server using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
