import base64
import json
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.logger import get_logger
from app.dsp.preprocessing import preprocess_pcm
from app.detection.matcher import match_template
from app.detection.templates_loader import load_templates

router = APIRouter()
logger = get_logger("websocket")

TEMPLATES = load_templates()

def decode_pcm(b64: str) -> np.ndarray:
    raw = base64.b64decode(b64)
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32)

@router.websocket("/ws/detect")
async def ws_detect(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")

    try:
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)

            pcm = decode_pcm(data["pcm_base64"])
            sr = data.get("sample_rate", 16000)

            pcm = preprocess_pcm(pcm, sr)

            result = match_template(pcm, TEMPLATES)

            await websocket.send_text(json.dumps(result))

    except WebSocketDisconnect:
        logger.info("Client disconnected")
