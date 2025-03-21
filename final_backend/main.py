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

# Create FastAPI instance
app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Endpoint for Audio Processing
@app.websocket("/audio-stream/")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")

    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            if not audio_chunk:
                logger.warning("Empty audio received, skipping processing.")
                continue

            # Convert speech to text
            text = await asyncio.to_thread(speech_to_text.process_chunk, audio_chunk)
            logger.info(f"Transcription: {text}")

            if not text.strip():
                logger.warning("No speech detected, skipping response.")
                await websocket.send_json({"error": "No speech detected."})
                continue

            # Analyze emotional tone
            emotion = await asyncio.to_thread(emotion_analysis.analyze_audio_chunk, audio_chunk)
            logger.info(f"Detected emotion: {emotion}")

            # Generate AI text response
            response = await asyncio.to_thread(text_response.generate_response, text, emotion)
            logger.info(f"Generated response: {response}")

            # Convert response to speech (Bytes)
            speech_bytes = await asyncio.to_thread(text_to_speech.convert_text_to_speech, response)
            if not speech_bytes:
                logger.error("Failed to generate speech output.")
                await websocket.send_json({"error": "Failed to generate audio response."})
                continue

            # Store session details in DB
            await asyncio.to_thread(database.store_entry, text, emotion, response)

            # Send JSON text response
            await websocket.send_json({
                "transcription": text,
                "emotion": emotion,
                "response": response
            })

            # Send audio response as base64
            audio_base64 = base64.b64encode(speech_bytes).decode("utf-8")
            await websocket.send_json({"audio_response": audio_base64})

            logger.info("Audio response sent successfully.")

    except WebSocketDisconnect:
        logger.info("Client disconnected.")
    except Exception as e:
        logger.error(f"Error in WebSocket: {e}")
    finally:
        await websocket.close()
        logger.info("WebSocket closed.")

# Fetch all diary entries
@app.get("/diary-entries/")
async def get_entries():
    try:
        entries = await asyncio.to_thread(database.get_entries)
        return {"entries": entries}
    except Exception as e:
        logger.error(f"Error fetching diary entries: {e}")
        return {"error": "Failed to fetch diary entries."}
