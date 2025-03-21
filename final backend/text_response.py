import requests

# Mistral 7B model running on Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"

# Emotion-based prompts to enhance response quality
EMOTION_PROMPTS = {
    "happy": "Be cheerful and encouraging.",
    "sad": "Be supportive and empathetic.",
    "angry": "Be calm and help the user find solutions.",
    "fearful": "Be reassuring and provide comfort.",
    "neutral": "Be neutral and conversational.",
    "excited": "Match the excitement and enthusiasm.",
    "frustrated": "Be understanding and offer guidance.",
    "lonely": "Be warm and comforting.",
}


def generate_response(text, emotion):
    """
    Generates a response based on the user's text and detected emotion using Mistral 7B.

    :param text: Transcribed text from speech
    :param emotion: Detected emotion (one of: happy, sad, angry, fearful, neutral, excited, frustrated, lonely)
    :return: AI-generated response string
    """

    # Default to neutral if emotion is not recognized
    emotion_prompt = EMOTION_PROMPTS.get(emotion, "Be neutral and conversational.")

    # Construct the LLM prompt
    prompt = f"""
    User is speaking with an AI diary. They just shared something personal.
    Their detected emotion is: {emotion}.
    
    Their message: "{text}"
    
    Your response should align with their emotion and situation. {emotion_prompt}
    Keep it concise and natural.
    """

    # Send request to Ollama
    response = requests.post(
        OLLAMA_URL,
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )

    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return "I'm here for you. Feel free to share more."
