import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Use Mistral instead of GPT-2
MODEL_NAME = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True, torch_dtype=torch.float16, device_map="auto")

# Emotion-based response styles
EMOTION_PROMPTS = {
    "happy": "Respond with joy and encouragement.",
    "sad": "Be empathetic and comforting.",
    "angry": "Remain calm and offer practical solutions.",
    "fearful": "Provide reassurance and safety.",
    "neutral": "Maintain a neutral and conversational tone.",
    "excited": "Match the excitement and enthusiasm.",
    "frustrated": "Be understanding and offer solutions.",
    "lonely": "Be warm and comforting.",
}

def generate_response(text, emotion):
    """
    Generates an AI response based on the user's text and detected emotion.
    """
    emotion_prompt = EMOTION_PROMPTS.get(emotion, "Maintain a neutral tone.")

    # ✅ Better, natural prompt structure
    prompt = f"""
    User: {text}
    Emotion: {emotion}
    AI ({emotion_prompt}): 
    """

    try:
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

        output_ids = model.generate(
            **inputs,
            max_new_tokens=100,  # Limits response length
            temperature=0.7,      # Balances creativity and coherence
            top_p=0.9,            # Nucleus sampling for diversity
            pad_token_id=tokenizer.eos_token_id
        )

        # ✅ Decode and clean the response
        generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

        # ✅ Remove any repeated prompt from the output dynamically
        if "AI (" in generated_text:
            generated_text = generated_text.split("AI (", 1)[-1].split("):", 1)[-1].strip()

        logger.info(f"Generated response: {generated_text}")
        return generated_text

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "I'm here for you. Feel free to share more."
