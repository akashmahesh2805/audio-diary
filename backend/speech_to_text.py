import whisper

def convert_audio_to_text(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]
