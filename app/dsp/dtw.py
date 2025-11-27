import librosa
from app.core.config import config

def dtw_distance(m1, m2):
    D, wp = librosa.sequence.dtw(X=m1, Y=m2, metric="euclidean")
    dist = D[-1, -1]
    if config.DTW_NORMALIZE and wp.shape[0] > 0:
        return dist / wp.shape[0]
    return dist
