from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import speech_to_text
import emotion_analysis
import text_response
import text_to_speech
import database
import asyncio
import logging
import base64
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://audio-diary-p1e4.vercel.app/"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# WebSocket endpoint for real-time audio streaming
@app.websocket("/audio-stream/")
async def audio_stream(websocket: WebSocket):
    
    await websocket.accept()
    logger.info("WebSocket connection established")

    try:
        while True:
            # Receive audio data from client
            audio_chunk = await websocket.receive_bytes()
            logger.info(f"Received audio chunk: {len(audio_chunk)} bytes")

            if not audio_chunk:
                logger.warning("Received an empty audio chunk, skipping processing.")
                continue

            # Convert audio to text using speech-to-text
            text = await asyncio.to_thread(speech_to_text.process_chunk, audio_chunk)
            logger.info(f"Transcription: {text}")

            if not text.strip():
                await websocket.send_json({"error": "No speech detected."})
                logger.warning("No speech detected, skipping processing.")
                continue

            # Analyze emotional tone
            emotion = await asyncio.to_thread(emotion_analysis.analyze_audio_chunk, audio_chunk)
            logger.info(f"Emotion detected: {emotion}")

            # Generate AI response
            response = await asyncio.to_thread(text_response.generate_response, text, emotion)
            logger.info(f"Generated response: {response}")

            # Convert response to speech (returns bytes)
            speech_bytes = await asyncio.to_thread(text_to_speech.convert_text_to_speech, response)

            if not speech_bytes:
                logger.error("Failed to generate speech output.")
                await websocket.send_json({"error": "Failed to generate audio response."})
                continue

            # Store session details in the database
            await asyncio.to_thread(database.store_entry, text, emotion, response)

            # Send JSON response first
            await websocket.send_json({
                "transcription": text,
                "emotion": emotion,
                "response": response
            })

            # Send binary audio response separately
            audio_base64 = base64.b64encode(speech_bytes).decode("utf-8")
            await websocket.send_json({"audio_response": audio_base64})

            logger.info("Audio response sent to client")

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {e}")
    finally:
        await websocket.close()
        logger.info("WebSocket closed.")

# Endpoint to retrieve all stored diary entries
@app.get("/diary-entries/")
async def get_entries():
    try:
        entries = await asyncio.to_thread(database.get_entries)
        return {"entries": entries}
    except Exception as e:
        logger.error(f"Error fetching diary entries: {e}")
        return {"error": "Failed to fetch diary entries."}
