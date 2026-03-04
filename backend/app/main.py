from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.spotify_client import (
    get_auth_url,
    get_access_token,
    get_liked_tracks,
    save_raw_json
)

from app.swipe_service import (
    get_top_recommendations,
    handle_swipe,
    get_next_track
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "MelodicMatch Backend Running"}


@app.get("/login")
def login():
    return RedirectResponse(get_auth_url())


@app.get("/callback")
def callback(code: str):
    token_data = get_access_token(code)

    if "access_token" not in token_data:
        return {"error": token_data}

    access_token = token_data["access_token"]

    liked_tracks = get_liked_tracks(access_token)

    save_raw_json(liked_tracks, "liked_tracks.json")

    return {
        "message": "Stage 1 complete",
        "tracks_pulled": len(liked_tracks)
    }
    
class SwipeRequest(BaseModel):
    track_id: str
    liked: bool


@app.get("/next-track")
def next_track():
    return get_next_track()


@app.post("/swipe")
def swipe_track(request: SwipeRequest):
    handle_swipe(request.track_id, request.liked)
    return {"message": "Swipe recorded"}


@app.get("/recommend")
def recommend(k: int = 5):
    return get_top_recommendations(k)