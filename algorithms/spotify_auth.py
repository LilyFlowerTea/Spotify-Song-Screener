import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# authorise

def spotify_auth():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                                   client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                                   redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
                                                   scope="playlist-read-private",
                                                   open_browser = True,
                                                   # cache_handler =
                                                   ))
    return sp