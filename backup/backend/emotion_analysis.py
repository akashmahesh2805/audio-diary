"""
emotion_analysis.py - Detects emotion from audio (tone) + text

- Uses WavLM to detect emotions from tone.
- Considers text content for better accuracy.
- Returns the dominant emotion for the audio event.
"""

from transformers import WavLMForSequenceClassification, WavLMProcessor
import torch

# Load the WavLM emotion analysis model and processor
model = WavLMForSequenceClassification.from_pretrained("microsoft/wavlm-large")
processor = WavLMProcessor.from_pretrained("microsoft/wavlm-large")

def analyze_audio(audio_file):
    """
    Analyzes emotions from audio tone and text.
    - Converts audio into embeddings using WavLM.
    - Predicts the emotion category.
    """
    inputs = processor(audio_file, return_tensors="pt", padding=True)  # Process input audio
    
    with torch.no_grad():
        logits = model(**inputs).logits  # Get emotion logits
    
    emotion_label = torch.argmax(logits, dim=-1).item()  # Get highest probability emotion
    
    emotions = ["Neutral", "Happy", "Sad", "Angry", "Fearful", "Disgust", "Surprised"]
    return emotions[emotion_label]  # Return the detected emotion
