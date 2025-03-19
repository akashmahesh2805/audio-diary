from gtts import gTTS
import io

def convert_text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    return audio_buffer.getvalue()
