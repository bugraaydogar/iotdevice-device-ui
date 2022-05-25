from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from .snapd import SnapdClient

app = FastAPI()
snap_client = SnapdClient()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/refresh")
def refresh():
    response = snap_client.refresh()
    return response


@app.post("/revert")
def revert(snaps: List[str]):
    response = snap_client.revert(snaps)
    return response

