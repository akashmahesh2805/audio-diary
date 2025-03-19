import torch
import torchaudio
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import confusion_matrix, classification_report
from torch.utils.data import DataLoader, Dataset

# Load and process audio
def analyze_audio(file_path='audio_sample.wav'):
    waveform, sample_rate = torchaudio.load(file_path)
    waveform = waveform / torch.max(torch.abs(waveform))  # Normalize

    # Convert to Mel Spectrogram
    mel_spec = torchaudio.transforms.MelSpectrogram(sample_rate)(waveform)

    # Convert to MFCC
    mfcc = torchaudio.transforms.MFCC(sample_rate)(waveform)

    # Plot Mel Spectrogram
    plt.figure(figsize=(10, 4))
    plt.imshow(torch.log1p(mel_spec)[0, :, :].detach().numpy(), cmap='inferno')
    plt.title('Mel Spectrogram')
    plt.show()

    return mel_spec, mfcc  # Return features for further processing

# Define Speech Emotion Model
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
        self.fc = nn.Linear(128, 6)  # 6 emotion classes

    def forward(self, x):
        x = self.cnn(x)
        x = x.view(x.size(0), -1, 64 * 8 * 8)  # Flatten properly
        x, _ = self.lstm(x)
        x = self.fc(x[:, -1, :])
        return x

# Initialize Model
model = SpeechEmotionModel()
print(model)

# Dummy Dataset (Replace with actual dataset)
class DummyAudioDataset(Dataset):
    def __init__(self, num_samples=100):
        self.data = torch.randn(num_samples, 1, 32, 32)  # Dummy spectrograms
        self.labels = torch.randint(0, 6, (num_samples,))  # 6 emotion classes

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# Data Loaders
train_loader = DataLoader(DummyAudioDataset(1000), batch_size=32, shuffle=True)
test_loader = DataLoader(DummyAudioDataset(200), batch_size=32, shuffle=False)

# Loss and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training Loop
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for audio, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(audio)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Evaluation
model.eval()
all_preds, all_labels = [], []
for audio, labels in test_loader:
    with torch.no_grad():
        outputs = model(audio)
        preds = torch.argmax(outputs, dim=1)
        all_preds.extend(preds.tolist())
        all_labels.extend(labels.tolist())

print(confusion_matrix(all_labels, all_preds))
print(classification_report(all_labels, all_preds))

# Save and Load Model
torch.save(model.state_dict(), 'speech_model.pth')
model.load_state_dict(torch.load('speech_model.pth'))
model.eval()  # Set to evaluation mode after loading
