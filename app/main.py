from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
app.include_router(router)
app.mount(
    "/front",
    StaticFiles(directory=BASE_DIR / "frontend", html=True),
    name="frontend",
)
