from fastapi import FastAPI
from scanner import scan_network

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/scan")
def scan():
    return scan_network()