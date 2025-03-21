import pyttsx3
import io
import logging
import wave

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speaking rate
engine.setProperty("volume", 1.0)  # Max volume

def convert_text_to_speech(response_text):
    """
    Converts AI-generated text to speech and returns audio as bytes.
    """
    try:
        logger.info("Generating speech output...")

        # Create in-memory buffer
        audio_buffer = io.BytesIO()

        # Save speech to a temporary file (pyttsx3 does not support direct byte output)
        temp_file = "response_audio.wav"
        engine.save_to_file(response_text, temp_file)
        engine.runAndWait()

        # Read the saved file into memory
        with open(temp_file, "rb") as f:
            audio_bytes = f.read()

        # Convert WAV to PCM format (optional)
        with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
            pcm_audio = wav_file.readframes(wav_file.getnframes())

        logger.info("TTS conversion successful")
        return pcm_audio  # Return raw PCM bytes (smaller than WAV)
    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {e}")
        return None
