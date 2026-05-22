from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.scanner import scan_network, enrich_devices
from app.db import init_db, save_devices, get_devices

app = FastAPI()

# DB
init_db()

# API
@app.get("/")
def root():
    return RedirectResponse(url="/ui")

@app.get("/scan")
async def scan():
    devices = scan_network()
    devices = await enrich_devices(devices)

    save_devices(devices)
    return devices

@app.get("/devices")
def devices():
    return get_devices()

# STATIC UI
app.mount("/ui", StaticFiles(directory="app/static", html=True), name="static")