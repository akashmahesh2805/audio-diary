from transformers import pipeline

emotion_classifier = pipeline("sentiment-analysis")

def analyze_text(text):
    result = emotion_classifier(text)[0]
    return {"emotion": result["label"], "confidence": result["score"]}
