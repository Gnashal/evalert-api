from app.dsp.mfcc import compute_mfcc
from app.dsp.dtw import dtw_distance
from app.core.config import config

def match_template(pcm, templates):
    incoming_mfcc = compute_mfcc(pcm)

    best_name = None
    best_score = float("inf")

    for name, tmpl_mfcc in templates:
        score = dtw_distance(incoming_mfcc, tmpl_mfcc)
        if score < best_score:
            best_score = score
            best_name = name

    detected = best_score < config.DETECTION_THRESHOLD
    confidence = 1 / (1 + best_score)

    return {
        "detected": detected,
        "template": best_name,
        "score": best_score,
        "confidence": confidence,
    }
