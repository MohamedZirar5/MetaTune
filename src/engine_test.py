import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

try:
    query = "The Legend of Zelda: Breath of the Wild OST"
    results = sp.search(q=query, type='album', limit=1)
    
    album_name = results['albums']['items'][0]['name']
    artist_name = results['albums']['items'][0]['artists'][0]['name']
    
    print(f"Found: {album_name} by {artist_name}")

except Exception as e:
    print(f"Error : {e}")