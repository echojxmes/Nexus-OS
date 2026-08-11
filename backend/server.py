from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from system import get_system_stats
from config import load_config, reload_config
from hardware import sensors, leds

app = FastAPI(title="NEXUS Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LedMode(BaseModel):
    mode: str


@app.get("/api/system")
def system_status():
    return get_system_stats()


@app.get("/api/environment")
def environment_status():
    return sensors.read_environment()


@app.get("/api/leds")
def leds_status():
    return leds.get_mode()


@app.post("/api/leds")
def set_leds(body: LedMode):
    return leds.set_mode(body.mode)


@app.get("/api/config")
def get_config():
    return load_config()


@app.post("/api/config/reload")
def reload_config_endpoint():
    return reload_config()


frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)