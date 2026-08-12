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

playlist_id = "https://open.spotify.com/playlist/2zWZnSHWMmEL0muWdFK8Ch"

results = sp.playlist_items(playlist_id)

for item in results['items']:
    track = item['item']
    print(track['name'], "-", track['artists'][0]['name'])