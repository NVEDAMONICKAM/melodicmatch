import base64
import requests
import json
import os
from app.config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    REDIRECT_URI,
    AUTH_URL,
    TOKEN_URL,
    API_BASE_URL
)

SCOPES = "user-library-read"

def get_auth_url():
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES
    }

    request = requests.Request("GET", AUTH_URL, params=params).prepare()
    print("AUTH URL:", request.url)  # ADD THIS
    return request.url


def get_access_token(code):
    auth_header = base64.b64encode(
        f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    return response.json()


def get_liked_tracks(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    tracks = []
    url = f"{API_BASE_URL}/me/tracks?limit=50"

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()

        tracks.extend(data["items"])
        url = data["next"]

    return tracks


def save_raw_json(data, filename):
    os.makedirs("data/raw", exist_ok=True)
    path = f"data/raw/{filename}"

    with open(path, "w") as f:
        json.dump(data, f, indent=2)