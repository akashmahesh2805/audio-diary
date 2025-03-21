import numpy as np
import io
import torch
import whisper
import soundfile as sf

# Load Whisper model
model = whisper.load_model("base")

def process_chunk(audio_bytes):
    """Processes audio chunk and converts to text."""
    try:
        # Convert bytes to NumPy array
        audio_np, sample_rate = sf.read(io.BytesIO(audio_bytes), dtype="float32")
        
        # Ensure correct shape and format
        if len(audio_np.shape) > 1:  
            audio_np = np.mean(audio_np, axis=1)  # Convert to mono
        
        # Transcribe using Whisper
        result = model.transcribe(audio_np, fp16=False)  # Disable FP16 for compatibility
        return result["text"]
    except Exception as e:
        print(f"❌ Error in speech_to_text: {e}")
        return "Error processing audio"