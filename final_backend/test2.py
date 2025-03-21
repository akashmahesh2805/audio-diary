import torch
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor

# Load model and feature extractor
model = Wav2Vec2ForSequenceClassification.from_pretrained("superb/wav2vec2-base-superb-er")
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("superb/wav2vec2-base-superb-er")

# Load and preprocess audio
import librosa
speech, _ = librosa.load("test_audio.wav", sr=16000, mono=True)
inputs = feature_extractor(speech, sampling_rate=16000, return_tensors="pt", padding=True)

# Run inference
with torch.no_grad():
    logits = model(**inputs).logits

# Get predicted emotion
predicted_id = torch.argmax(logits, dim=-1).item()
predicted_emotion = model.config.id2label[predicted_id]

print(f"Predicted Emotion: {predicted_emotion}")
