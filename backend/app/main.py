from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .snapd import SnapdClient

class Snap(BaseModel):
    name: str

class Sequence(BaseModel):
    name: str

app = FastAPI()
snap_client = SnapdClient()

origins = [
    "*"
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
def revert(snap: Snap):
    print(snap.name)
    response = snap_client.revert(snap.name)
    return response


@app.get("/list")
def list():
    response = snap_client.list()
    return response


@app.post("/enforce")
def enforce(seq: Sequence):
    response = snap_client.enforce_validation(seq.name)
    return response

@app.post("/forget")
def forget():
    response = snap_client.forget_validation()
    return response

