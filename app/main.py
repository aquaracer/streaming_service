import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.streaming.handlers import router as streaming_router

app = FastAPI()

app.include_router(streaming_router)
STATIC_DIR = os.path.abspath("media/hls")
app.mount("/hls", StaticFiles(directory=STATIC_DIR), name="hls")
