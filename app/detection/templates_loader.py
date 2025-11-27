import os
import soundfile as sf
import librosa
import numpy as np

from app.core.config import config
from app.core.logger import get_logger
from app.dsp.mfcc import compute_mfcc

logger = get_logger("templates-loader")

def load_templates():
    templates = []
    if not os.path.isdir(config.TEMPLATE_DIR):
        os.makedirs(config.TEMPLATE_DIR)
        logger.warning(f"Template dir created at {config.TEMPLATE_DIR}. Add WAV files.")

    for fname in os.listdir(config.TEMPLATE_DIR):
        if not fname.lower().endswith(".wav"):
            continue

        path = os.path.join(config.TEMPLATE_DIR, fname)
        y, sr = sf.read(path)
        if sr != config.SAMPLE_RATE:
            y = librosa.resample(y, orig_sr=sr, target_sr=config.SAMPLE_RATE)

        if y.ndim == 2:
            y = np.mean(y, axis=1)

        mfcc = compute_mfcc(y)
        templates.append((fname, mfcc))

        logger.info(f"Loaded template '{fname}' MFCC.shape={mfcc.shape}")

    if not templates:
        logger.warning("No templates loaded!")

    return templates
