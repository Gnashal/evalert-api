from collections import deque
from app.dsp.spectral_flux import flux_features
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("detector")

# increase to 1 more second or longer when outside
WINDOW_SECONDS = 3.0 
FRAMES_IN_WINDOW = int((WINDOW_SECONDS * 1000) / settings.BUFFER_MS)

class SirenDetector:
    def __init__(self):
        self.history = deque(maxlen=FRAMES_IN_WINDOW)
        self.active = False

    def process(self, pcm):
        feats = flux_features(pcm, settings.SAMPLE_RATE)
        self.history.append(feats)

        if len(self.history) < self.history.maxlen:
            return None  # not enough data yet

        avg_flux = sum(f["mean"] for f in self.history) / len(self.history)
        avg_peaks = sum(f["peaks"] for f in self.history) / len(self.history)

        logger.info(
            f"[FLUX] mean={avg_flux:.2f} peaks={avg_peaks:.1f} active={self.active}"
        )

        # --- Detection rule ---
        detected = avg_flux > 0.005 and avg_peaks >= 1
        
        # Higher threshold and require more peaks
        # detected = avg_flux > 0.02 and avg_peaks >= 2



        if detected and not self.active:
            self.active = True
            return "EV_DETECTED"

        if not detected and self.active:
            self.active = False
            return "EV_CLEARED"

        return None
