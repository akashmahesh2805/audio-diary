import subprocess

def convert_text_to_speech(text):
    """Converts text to speech using Piper TTS (open-source)."""
    command = ["piper", "--model", "en_US", "--text", text, "--output", "output.wav"]
    subprocess.run(command)
    return "output.wav"
