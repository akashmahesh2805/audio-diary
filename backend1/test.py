import torch
import torchaudio
import torch.nn as nn

# Load the trained model
class SpeechEmotionModel(nn.Module):
    def __init__(self):
        super(SpeechEmotionModel, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.lstm = nn.LSTM(64 * 8 * 8, 128, batch_first=True)
        self.fc = nn.Linear(128, 6)  # 6 classes for emotions

    def forward(self, x):
        x = self.cnn(x)
        x = x.view(x.size(0), -1, x.size(1))
        x, _ = self.lstm(x)
        x = self.fc(x[:, -1, :])
        return x

# Load the saved model weights
model = SpeechEmotionModel()
model.load_state_dict(torch.load("speech_model.pth"))
model.eval()  # Set to evaluation mode

# Function to preprocess an audio file
def preprocess_audio(file_path):
    waveform, sample_rate = torchaudio.load(file_path)
    mel_spec = torchaudio.transforms.MelSpectrogram(sample_rate)(waveform)
    mel_spec = mel_spec.unsqueeze(0)  # Add batch dimension (1, 1, freq_bins, time_steps)
    return mel_spec

# Path to the test audio file
test_audio_path = "test_sample.wav"

# Preprocess the test audio
input_audio = preprocess_audio(test_audio_path)

# Run inference
with torch.no_grad():
    output = model(input_audio)

# Convert output to predicted class
predicted_class = torch.argmax(output, dim=1).item()

# Emotion labels (update based on dataset)
emotion_labels = ["Neutral", "Happy", "Sad", "Angry", "Fearful", "Surprised"]

# Print the prediction
print(f"Predicted Emotion: {emotion_labels[predicted_class]}")
