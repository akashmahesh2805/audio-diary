import numpy as np
import io
import torch
import whisper
import logging
import librosa
import soundfile as sf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Whisper model
model = whisper.load_model("base")

def process_chunk(audio_bytes):
    """Processes an audio chunk and converts it to text."""
    try:
        logger.info("Processing audio chunk...")

        # Convert bytes to NumPy array
        audio_np, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=None, mono=True)
        logger.info(f"Loaded audio: {audio_np.shape}, Sample rate: {sample_rate}")

        # Resample audio to 16 kHz (Whisper requirement)
        if sample_rate != 16000:
            audio_np = librosa.resample(audio_np, orig_sr=sample_rate, target_sr=16000)

        # Ensure exactly 30 seconds of audio (pad or truncate)
        target_length = 30 * 16000  # 30 seconds * 16000 Hz
        if len(audio_np) > target_length:
            audio_np = audio_np[:target_length]  # Truncate
        else:
            audio_np = np.pad(audio_np, (0, target_length - len(audio_np)), mode='constant')  # Pad

        # Transcribe using Whisper
        result = model.transcribe(audio_np, fp16=False, language="en")
        transcription = result.get("text", "").strip()
        logger.info(f"Transcription successful: {transcription}")
        return transcription if transcription else "No speech detected."
    
    except Exception as e:
        logger.error(f"Error in speech_to_text: {e}")
        return "Error processing audio."
