from fastapi import FastAPI
from scanner import scan_network
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/scan")
async def scan():
    devices = scan_network()
    return await enrich_devices(devices)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")