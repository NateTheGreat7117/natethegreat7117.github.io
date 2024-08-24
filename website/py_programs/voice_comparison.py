from sklearn.metrics.pairwise import cosine_similarity
import torch.nn.functional as F
import torch.nn as nn
import torchaudio
import torch

from py_programs.audio_processing import create_spect
import librosa
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

fs = 16000
n_mels = 128
win_length = 160
hop_length = 80
max_length = 8000

class ActDropNormCNN1D(nn.Module):
    def __init__(self, n_feats, dropout, keep_shape=False):
        super(ActDropNormCNN1D, self).__init__()
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(n_feats)
        self.keep_shape = keep_shape
    
    def forward(self, x):
        x = x.transpose(1, 2)
        # x = self.norm(self.dropout(F.gelu(x)))
        x = self.dropout(F.gelu(self.norm(x)))
        if self.keep_shape:
            return x.transpose(1, 2)
        else:
            return x

class SpeechDetection(nn.Module):
    def __init__(self, hidden_size, n_feats, num_layers, dropout):
        super(SpeechDetection, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.cnn1 = nn.Sequential(
            nn.Conv1d(128, n_feats, 10, 2, padding=10//2),
            ActDropNormCNN1D(n_feats, dropout, keep_shape=True),
        )
        self.cnn2 = nn.Sequential(
            nn.Conv1d(n_feats, n_feats, 10, 2, padding=10//2),
            ActDropNormCNN1D(n_feats, dropout, keep_shape=True),
        )
        self.cnn3 = nn.Sequential(
            nn.Conv1d(n_feats, n_feats, 10, 2, padding=10//2),
            ActDropNormCNN1D(n_feats, dropout, keep_shape=True),
        )
        self.cnn4 = nn.Sequential(
            nn.Conv1d(n_feats, n_feats, 10, 2, padding=10//2),
            ActDropNormCNN1D(n_feats, dropout),
        )
        self.lstm = nn.LSTM(input_size=n_feats, hidden_size=n_feats,
                            num_layers=self.num_layers, dropout=0.0,
                            bidirectional=False)
        self.dense = nn.Sequential(
            nn.Linear(n_feats*14, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(128, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(dropout),
        )
        
        self.layer_norm2 = nn.LayerNorm(128)
        self.dropout2 = nn.Dropout(dropout)
        self.final_fc = nn.Linear(128, 1)
        self.sigmoid = nn.Sigmoid()

    def _init_hidden(self, batch_size):
        n, hs = self.num_layers, self.hidden_size
        return (torch.zeros(n*1, batch_size, hs).to(device),
                torch.zeros(n*1, batch_size, hs).to(device))

    def forward(self, x, hidden):
        x = x.to(device)
        x = self.cnn1(x) # batch, channels, time, feature
        x = self.cnn2(x)
        x = self.cnn3(x)
        x = self.cnn4(x)
#         x, _ = self.lstm(x)
        x = torch.flatten(x, 1)
        x = self.dense(x) # batch, time, feature
        x = self.dropout2(F.relu(self.layer_norm2(x)))  # (time, batch, n_class)
        return self.sigmoid(self.final_fc(x))
    

class EmbeddingNet(nn.Module):
    def __init__(self, n_feats, dropout):
        super(EmbeddingNet, self).__init__()
        self.cnn1 = nn.Sequential(
            nn.Conv1d(128, n_feats, 10, 2, padding=10//2),
            ActDropNormCNN1D(n_feats, dropout, keep_shape=True),
        )
        self.cnn2 = nn.Sequential(
            nn.Conv1d(n_feats, n_feats, 10, 2, padding=10//2),
            ActDropNormCNN1D(n_feats, dropout, keep_shape=True),
        )    
        self.flatten = nn.Flatten()
        
        self.fc = nn.Sequential(
            nn.Linear(3072, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 128)
        )

    def forward(self, x):
        x = x.to(device)
        x = F.relu(F.max_pool1d(self.cnn1(x), 2))
        x = F.relu(F.max_pool1d(self.cnn2(x), 2))
        x = self.flatten(x)
        
        x = self.fc(x)
        
        return F.normalize(x, p=2, dim=1)  # Normalize embeddings

class VoiceComparison(nn.Module):
    def __init__(self, embedding_net):
        super(VoiceComparison, self).__init__()
        
        self.embedding_net = embedding_net
        
    def forward(self, anchor, positive, negative):
        anchor_embedding = self.embedding_net(anchor)
        positive_embedding = self.embedding_net(positive)
        negative_embedding = self.embedding_net(negative)
        return anchor_embedding, positive_embedding, negative_embedding

speech_detection = torch.jit.load("/home/nathanmon/Artificial Intelligence/PyTorch/Audio Recognition/Voice Classification/speech_detection.pth")
speaker_verification = torch.jit.load("/home/nathanmon/Artificial Intelligence/PyTorch/Audio Recognition/Voice Classification/speaker_verification.pth")

def detect_speech(spect):
    return speech_detection(spect, torch.tensor([]))[0][0]


def verify_speech(embedding_1, mel_spec_2):
    speaker_verification.eval()
    with torch.no_grad():
        # mel_spec_1 = torch.unsqueeze(mel_spec_1[0], 0)#.to(device)
        mel_spec_2 = torch.unsqueeze(mel_spec_2[0], 0)#.to(device)
        # embedding_1 = speaker_verification.embedding_net(mel_spec_1)
        embedding_2 = speaker_verification.embedding_net(mel_spec_2)
    # duration = librosa.get_duration(filename=mel_spec_2)
    # excerpt = Segment(duration-1, duration)
    
    # embedding_2 = model.crop(mel_spec_2, excerpt)
        
    similarity = cosine_similarity(embedding_1.cpu().numpy(), embedding_2.cpu().numpy())
    return similarity


def load_speaker_embeddings():
    speaker_embeddings = []
    speakers = os.listdir("/home/nathanmon/Artificial Intelligence/PyTorch/Jarvis/speaker_files/")
    with torch.no_grad():
        for speaker in speakers:
            waveform, padded_wav, speaker_spect = create_spect(f"/home/nathanmon/Artificial Intelligence/PyTorch/Jarvis/speaker_files/{speaker}", max_length, 8000, n_mels, 
                                                    win_length, hop_length)
            speaker_embeddings.append(speaker_verification.embedding_net(speaker_spect.to(device)))
        #     speaker_embeddings.append(speaker_verification(f"/home/nathanmon/Artificial Intelligence/PyTorch/Jarvis/speaker_files/{speaker}"))
    return speakers, speaker_embeddings