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
id_list = {}

# #pull target song
track_id = "https://open.spotify.com/track/5vYaBqOAT6JpZlAD3gO1AO"
# track_id = input("Paste track URL here: ")
target_track = sp.track(track_id)
print(f"Target song name is: {target_track["name"]}")
#I know I could split the user input, doing this to check everything's working fine
track_name = target_track['name']
track_id = target_track['id']
id_list[track_name] = track_id

#chaff from testing
# import pandas as pd
# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
# print(pd.DataFrame(target_track["album"]["artists"]))

#pull target playlist
playlist_id = "https://open.spotify.com/playlist/2Ehv3hyQ19J0n3VP0Fd9bN"
# playlist_id = input("Paste playlist URL here: ")
target_playlist = sp.playlist(playlist_id)
print(f"Target playlist name is: {target_playlist["name"]}")
results = sp.playlist_items(playlist_id)

for object in results['items']:
    track = object['item']
    track_id = track['id']
    # print(track_id)
    id_list[track['name']] = track_id
    # List playlist songs, could be removed
    # print(track['name'], "-", track['artists'][0]['name'])

ids = list((id_list.values()))

#Visualisation of progress
import pandas as pd
# df = pd.DataFrame(id_list.items(), columns = ["Song", "Spotify ID"])
# print(df)

#Parcelling out the track IDs into 5s and also formatting so they are accepted by audio feature extraction API
pcls = {}
index = 0
parcel = f""
count = 0
for id in range(len(ids)):
    parcel += f"{ids[id]}, "
    count += 1
    if count == 5:
        pcls[index] = parcel
        index += 1
        parcel = ""
        count = 0

#Now start pulling audio features
#Query string has been built, named ids
# querystring = {"ids" : ids}
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
# print(response)
# print(response.json())