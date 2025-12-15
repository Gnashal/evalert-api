import numpy as np
import librosa
from app.core.config import settings

def preprocess_pcm(pcm: np.ndarray, sr: int) -> np.ndarray:
    if pcm.shape[0] < settings.BUFFER_SAMPLES:
        pcm = np.pad(pcm, (0, settings.BUFFER_SAMPLES - pcm.shape[0]))
    else:
        pcm = pcm[:settings.BUFFER_SAMPLES]
    return pcm.astype(np.float32)

