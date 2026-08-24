#setting up
import spotipy
import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

#authorise
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                               client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                               redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
                                               scope="user-library-read"))

# Build query string for audio feature extraction later
# Start with target track, then append playlist tracks
id_list = []

#pull target song
track_id = input("Paste track URL here: ")
target_track = sp.track(track_id)
print(f"Target song name is: {target_track["name"]}")

#chaff from testing
# import pandas as pd
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
# print(pd.DataFrame(target_track["album"]["artists"]))

#pull target playlist
playlist_id = input("Paste playlist URL here: ")
target_playlist = sp.playlist(playlist_id)
print(f"Target playlist name is: {target_playlist["name"]}")
results = sp.playlist_items(playlist_id)
for object in results['items']:
    track = object['item']
    # id_list.append()
    # List playlist songs, could be removed
    print(track['name'], "-", track['artists'][0]['name'])

#Now start pulling audio features
#Query string was built in playlist_pull, id_list



# querystring = {"ids":"0DiWol3AO6WpXZgp0goxAV,1NeLwFETswx8Fzxl2AFl91"}
#
# url = "https://spotify-extended-audio-features-api.p.rapidapi.com/v1/audio-features"
# headers = {
# 	"x-rapidapi-key": os.environ["RAPID_API_KEY"],
# 	"x-rapidapi-host": os.environ["RAPID_API_HOST"],
# 	"Content-Type": "application/json"
# }
#
# import requests
# response = requests.get(url, headers=headers, params=querystring)
#
# print(response.json())