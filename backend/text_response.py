"""
text_response.py - Generates AI response using Mistral 7B

- Uses both detected emotion and text content to generate responses.
- Fine-tunes the prompt for better conversational quality.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load Mistral 7B model and tokenizer
model_name = "mistralai/Mistral-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

def generate_response(text, emotion):
    """
    Generates an AI response based on emotion + text.
    - Forms a structured prompt.
    - Uses Mistral 7B to generate a response.
    """
    prompt = f"User feels '{emotion}' about '{text}'. Provide an appropriate response."
    
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        output = model.generate(**inputs, max_length=100)  # Generate response
    
    return tokenizer.decode(output[0], skip_special_tokens=True)  # Return clean text
