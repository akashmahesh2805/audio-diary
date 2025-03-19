from transformers import pipeline

# Load a free, open-source LLM (Mistral 7B)
generator = pipeline("text-generation", model="mistralai/Mistral-7B-v0.1")

def generate_response(emotion_results):
    """
    Generate a supportive response based on the detected emotion.
    
    Args:
        emotion_results (dict): Emotion analysis results with keys 'emotion' and 'confidence'.
    
    Returns:
        str: AI-generated response.
    """
    prompt = f"The user feels {emotion_results['emotion']}. Generate a supportive and empathetic response."

    response = generator(prompt, max_length=50, num_return_sequences=1)
    
    return response[0]["generated_text"]

# Example usage
if __name__ == "__main__":
    test_emotion = {"emotion": "sad", "confidence": 0.95}
    print(generate_response(test_emotion))
