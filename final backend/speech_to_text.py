import numpy as np
import io
import torch
import whisper
import soundfile as sf

# Load Whisper model (assuming it's already loaded somewhere)
model = whisper.load_model("base")

def process_chunk(audio_bytes):
    """Processes audio chunk and converts to text."""
    try:
        # Convert bytes to NumPy array (properly formatted for Whisper)
        audio_np, sample_rate = sf.read(io.BytesIO(audio_bytes), dtype="float32")
        
        # Ensure correct shape and format
        if len(audio_np.shape) > 1:  
            audio_np = np.mean(audio_np, axis=1)  # Convert to mono
        
        # Convert to Whisper's required format (if needed)
        audio_tensor = torch.tensor(audio_np)

        # Transcribe using Whisper
        result = model.transcribe(audio_tensor.numpy())

        return result["text"]
    except Exception as e:
        print(f"❌ Error in speech_to_text: {e}")
        return "Error processing audio"
