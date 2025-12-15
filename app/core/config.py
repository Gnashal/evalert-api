import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SAMPLE_RATE = 16000
    BUFFER_MS = 500
    BUFFER_SAMPLES = int(SAMPLE_RATE * BUFFER_MS / 1000)
    N_MFCC = 13
    DETECTION_THRESHOLD = 4.0
    DTW_NORMALIZE = True

    TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")  

settings = Config()