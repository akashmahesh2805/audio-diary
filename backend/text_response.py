import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_response(emotion_results):
    prompt = f"The user feels {emotion_results['emotion']}. Generate a supportive response."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]
