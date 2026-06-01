import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def main():
    load_dotenv()
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not CLIENT_ID or not CLIENT_SECRET:
        print("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET in .env; please set them and retry.")
        return

    try:
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=10)

        query = "The Legend of Zelda: Breath of the Wild OST"
        results = sp.search(q=query, type="album", limit=1)
        items = results.get("albums", {}).get("items", [])
        if not items:
            print(f"No album results for query: {query}")
            return

        album = items[0]
        album_name = album.get("name", "Unknown")
        artist_name = (album.get("artists") or [{}])[0].get("name", "Unknown")

        print(f"Found: {album_name} by {artist_name}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()