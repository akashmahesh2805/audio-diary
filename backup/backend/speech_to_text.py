"""
speech_to_text.py - Converts audio to text

- Uses Wav2Vec2 for high-quality speech-to-text conversion.
- Processes raw audio bytes and extracts transcriptions.
"""

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torchaudio
import torch

# Load Wav2Vec2 model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def convert_audio_to_text(audio_bytes):
    """
    Converts raw audio bytes into transcribed text.
    - Loads audio into a waveform.
    - Runs through Wav2Vec2 for transcription.
    """
    waveform, sample_rate = torchaudio.load(audio_bytes)  # Convert bytes to waveform
    inputs = processor(waveform.squeeze(0), sampling_rate=sample_rate, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        logits = model(inputs.input_values).logits  # Predict speech tokens
    
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]  # Convert tokens to text
    return transcription
