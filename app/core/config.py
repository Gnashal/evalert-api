import os

class Config:
    SAMPLE_RATE = 16000
    BUFFER_MS = 250
    BUFFER_SAMPLES = int(SAMPLE_RATE * BUFFER_MS / 1000)
    N_MFCC = 13
    DETECTION_THRESHOLD = 0.45
    DTW_NORMALIZE = True

    TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates")

config = Config()
