import io
import numpy as np
import logging
import librosa
import torch
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Load the model from Hugging Face Hub
MODEL_NAME = "superb/wav2vec2-base-superb-er"
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_NAME)

# ✅ Get emotion labels dynamically from model
EMOTION_LABELS = model.config.id2label  # This ensures labels are correct

def analyze_emotion(audio_bytes):
    """Analyzes emotion from an audio chunk using a pre-trained model."""
    try:
        logger.info("Analyzing audio chunk...")

        # Convert bytes to NumPy array (Auto-detect sample rate)
        audio_np, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=None, mono=True)
        logger.info(f"Loaded audio: {audio_np.shape}, Sample rate: {sample_rate}")

        # ✅ Resample audio to 16 kHz (Required for Wav2Vec2)
        if sample_rate != 16000:
            audio_np = librosa.resample(audio_np, orig_sr=sample_rate, target_sr=16000)

        # ✅ Pad short segments (Ensure at least 3 seconds)
        min_duration = 3.0  # Minimum 3 seconds
        required_samples = int(16000 * min_duration)  # 3 sec * 16000 Hz
        if len(audio_np) < required_samples:
            logger.warning("Audio too short. Padding with silence.")
            audio_np = np.pad(audio_np, (0, required_samples - len(audio_np)), mode="constant")

        # Process the audio with the pre-trained model
        inputs = feature_extractor(audio_np, sampling_rate=16000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
            predicted_class = torch.argmax(logits, dim=-1).item()

        # ✅ Get the correct emotion label
        predicted_emotion = EMOTION_LABELS.get(predicted_class, "neutral")

        logger.info(f"Emotion detected: {predicted_emotion}")
        return predicted_emotion

    except Exception as e:
        logger.error(f"Error in emotion analysis: {e}")
        return "neutral"  # Default to neutral if an error occurs
