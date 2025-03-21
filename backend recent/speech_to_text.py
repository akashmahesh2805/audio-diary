import whisper

# Load Whisper model
model = whisper.load_model("base")

def process_chunk(audio_chunk):
    """Converts audio chunk to text using Whisper ASR."""
    result = model.transcribe(audio_chunk)
    return result["text"]
