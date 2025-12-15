import json
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.logger import get_logger
from app.dsp.preprocessing import preprocess_pcm
from app.detection.detector import SirenDetector

router = APIRouter()
logger = get_logger("websocket")

detector = SirenDetector() 


@router.websocket("/ws")
async def ws_detect(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")

    try:
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)

            pcm = np.array(data["audio"], dtype=np.float32)

            sr = data.get("sample_rate", 16000)
            rms = data.get("rms")
            timestamp = data.get("timestamp")

            pcm = preprocess_pcm(pcm, sr)
            pcm = pcm * 2.0
            event = detector.process(pcm)
            
            # Un-comment this if outside env
            # rms = np.sqrt(np.mean(pcm**2))
            # if rms < 0.01:  # if very quiet, ignore frame
            #     return None
            # pcm = pcm / (rms + 1e-8)  # normalize so flux is meaningful

            logger.debug(f"PCM max={np.max(np.abs(pcm)):.4f} mean={np.mean(np.abs(pcm)):.4f}")
            if event is not None:
                response = {
                    "type": event,  # EV_DETECTED or EV_CLEARED
                    "timestamp": timestamp,
                    "rms": rms,
                }
                logger.info(f"Detector event: {event}")
                await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception:
        logger.exception("WebSocket error")
        await websocket.close()
