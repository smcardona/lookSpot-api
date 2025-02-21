import os
import time
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

# Credenciales de Spotify
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Variables para el token
API_TOKEN = None
TOKEN_EXPIRATION = 0

def get_spotify_token():
  global API_TOKEN, TOKEN_EXPIRATION
  
  # Verifica si el token es válido
  if API_TOKEN and time.time() < TOKEN_EXPIRATION:
    return API_TOKEN
  
  # Solicita un nuevo token
  url = "https://accounts.spotify.com/api/token"
  data = {"grant_type": "client_credentials"}
  auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
  
  response = requests.post(url, data=data, auth=auth)
  
  if response.status_code == 200:
    token_data = response.json()
    API_TOKEN = token_data["access_token"]
    TOKEN_EXPIRATION = time.time() + token_data["expires_in"]
    print(API_TOKEN)
    print(TOKEN_EXPIRATION)
    return API_TOKEN
  else:
    raise Exception(f"Error obteniendo el token: {response.status_code} - {response.text}")


def get_track(id: str):
  url = f"https://api.spotify.com/v1/tracks/{id}"
  headers = {
    "Authorization": f"Bearer {get_spotify_token()}"
  }
  
  response = requests.get(url, headers=headers)
  
  if response.status_code == 200:
    res = response.json()
    return get_track_data(res)
  elif response.status_code == 404:
    return None
  else:
    print(response.status_code)
    raise Exception(f"Error obteniendo la pista: {response.status_code} - {response.json()["error"]["message"]}")
  
  
def find_track(name: str, quantity: int = 1):
  url = f"https://api.spotify.com/v1/search?q={name}&type=track&limit={quantity}"
  headers = {
    "Authorization": f"Bearer {get_spotify_token()}"
  }
  
  response = requests.get(url, headers=headers)
  
  if response.status_code == 200:
    res = response.json()
    items = res["tracks"]["items"]
    
    if len(items) > 1:
      return [get_track_data(items[i]) for i in range(len(items))]
    elif len(items) == 1:
      return [get_track_data(items[0])]
    else: 
      return None
    
    
    
  elif response.status_code == 404:
    return None
  else:
    print(response.status_code)
    raise Exception(f"Error obteniendo la pista: {response.status_code} - {response.json()["error"]["message"]}")
  
  
  
  
  
  
def get_track_data(data):
  return {
      "id": data["id"],
      "name": data["name"],
      "image": data["album"]["images"][0]["url"] if data["album"]["images"] else None,
      "artist": data["artists"][0]["name"] if data["artists"] else None,
      "link": data["external_urls"]["spotify"]
    }
  