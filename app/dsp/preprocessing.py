import numpy as np
import librosa
from app.core.config import config

def preprocess_pcm(pcm: np.ndarray, sr: int) -> np.ndarray:
    # resample if needed
    if sr != config.SAMPLE_RATE:
        pcm = librosa.resample(pcm, orig_sr=sr, target_sr=config.SAMPLE_RATE)

    # pad or trim to expected length
    if pcm.shape[0] < config.BUFFER_SAMPLES:
        pcm = np.pad(pcm, (0, config.BUFFER_SAMPLES - pcm.shape[0]))
    else:
        pcm = pcm[:config.BUFFER_SAMPLES]

    # normalize [-1,1]
    if pcm.dtype != np.float32:
        pcm = pcm.astype(np.float32)
    pcm = pcm / (np.max(np.abs(pcm)) + 1e-8)

    return pcm
