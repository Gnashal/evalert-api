import librosa
import numpy as np
from app.core.config import config

def compute_mfcc(pcm: np.ndarray) -> np.ndarray:
    y = librosa.effects.preemphasis(pcm)
    mfcc = librosa.feature.mfcc(
        y=y,
        sr=config.SAMPLE_RATE,
        n_mfcc=config.N_MFCC,
        n_fft=1024,
        hop_length=256,
    )
    mfcc = (mfcc - np.mean(mfcc, axis=1, keepdims=True)) / (
        np.std(mfcc, axis=1, keepdims=True) + 1e-8
    )
    return mfcc
