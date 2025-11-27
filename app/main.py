from fastapi import FastAPI
from app.api.websocket import router as ws_router

app = FastAPI()

app.include_router(ws_router)
