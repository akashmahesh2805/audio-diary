"""
text_to_speech.py - Converts text response into speech

- Uses VITS (Vocoder-based Text-to-Speech) from torch + torchaudio.
- Outputs an audio file for playback.
"""

import torch
import torchaudio
import torchaudio.pipelines as pipelines

# Load a pre-trained text-to-speech model (VITS from torchaudio)
bundle = pipelines.TACOTRON2_WAVERNN_PHONE_LJSPEECH
processor = bundle.get_text_processor()
tacotron2 = bundle.get_tacotron2()
vocoder = bundle.get_vocoder()

def convert_text_to_speech(text, output_path="response.wav"):
    """
    Converts input text to speech using an offline VITS model.
    Saves the audio as a .wav file and returns the file path.
    """
    # Convert text to tensor
    processed_text = processor(text)

    # Generate spectrogram using Tacotron2
    with torch.no_grad():
        mel_spec, _, _ = tacotron2.infer(processed_text)

    # Convert spectrogram to waveform using the vocoder
    with torch.no_grad():
        waveforms = vocoder(mel_spec)

    # Save the generated audio
    torchaudio.save(output_path, waveforms.cpu(), sample_rate=bundle.sample_rate)
    
    return output_path  # Return the file path for further use
