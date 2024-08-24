import numpy as np
import torchaudio
import pyaudio
import torch
import wave
import time
import os

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 16000
seconds = 10
filename = "temp.wav"
frames = []

p = pyaudio.PyAudio()

n_mels = 128
win_length = 160
hop_length = 80
max_length = 8000

def create_spect(filename, max_length, target_sr, n_mels, win_length, hop_length):
    original_waveform, current_sr = torchaudio.load(filename)
    waveform = torchaudio.functional.resample(original_waveform, current_sr, target_sr)
    if len(waveform[0]) < max_length:
        padded_wav = torch.concat((waveform[0], torch.zeros(max_length - len(waveform[0])))).unsqueeze(-2)
    else:
        cut_length = len(waveform[0]) - max_length
#         padded_wav = waveform[0][cut_length//2:len(waveform[0])-(cut_length//2)].unsqueeze(-2)
        padded_wav = waveform[0][cut_length:].unsqueeze(-2)
        
    spect = torchaudio.transforms.MelSpectrogram(
                                sample_rate=current_sr, n_mels=n_mels,
                                win_length=win_length, 
                                hop_length=hop_length)(padded_wav)
    spect = np.log(spect + 1e-14)
        
    return original_waveform, padded_wav, spect

def reset_audio(filename, sleep=True):
    os.remove(filename)
    if sleep:
        time.sleep(3)
    return [], 0

def save(waveform):
    wf = wave.open(filename, "wb")
    # set the channels
    wf.setnchannels(1)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(sample_format))
    # set the sample rate
    wf.setframerate(16000)
    # write the frames as bytes
    wf.writeframes(b"".join(waveform))
    # close the file
    wf.close()