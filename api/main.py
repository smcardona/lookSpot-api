from fastapi import FastAPI, HTTPException
from api.spotify_manager import get_track, find_track
from api.gemini_manager import wonder_songs
from urllib.parse import quote

from api.user import router as user_router
from api.album import router as album_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(album_router)

@app.get("/track/{id}")
async def read_track(id: str):
  try:
    track = get_track(id)
    if not track:
      raise HTTPException(status_code=404, detail="Track not found")
    return track
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  

@app.get("/app/ask/{query}")
async def calc_tracks(query: str):
  
  songs_names = wonder_songs(query)
  quantity_to_fetch = 2 if len(songs_names) < 3 else 1
  result = []
  for song_name in songs_names:
    tracks = find_track(song_name, quantity_to_fetch)
    if tracks:
      result.extend(tracks)
  return result
  


@app.get("/app/search/{name}")
async def search_track(name: str):
  try:
    formatted_name = quote(name)
    track = find_track(formatted_name)
    if not track:
      raise HTTPException(status_code=404, detail="Track not found")
    return track[0]
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))