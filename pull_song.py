import spotipy
import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                               client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                               redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
                                               scope="user-library-read"))

playlist_id = input("Paste playlist URL here: ")

playlist = sp.playlist(playlist_id)
results = sp.playlist_items(playlist_id)

print(f"Playlist name is: {playlist["name"]}")

for object in results['items']:
    track = object['item']
    print(track['name'], "-", track['artists'][0]['name'])