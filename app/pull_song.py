#setting up
import spotipy
import os
from pathlib import Path
import requests
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#pull target song, returns song ID in a dictionary
def pull_target_track(sp, id_dict, track_url):
    target_track = sp.track(track_url)
    track_name = target_track["name"]
    track_id = target_track["id"]
    id_dict["target"][track_name] = track_id
    return track_name, id_dict

#pull target playlist
def pull_playlist(sp, id_dict, playlist_url):
    if "playlist" in playlist_url:
        target_playlist = sp.playlist(playlist_url)
        playlist_name = target_playlist["name"]
        results = sp.playlist_items(playlist_url)
        # Collect playlist track IDs and names
        for obj in results["items"]:
            track = obj["item"]
            track_id = track["id"]
            id_dict["playlist tracks"][track["name"]] = track_id
            # Line below is no longer necessary, just reverse id_dict to get song names
            # Could be used if I wanted artist name as well
            # name_list.append((track['name'], track['artists'][0]['name']))
    elif "album" in playlist_url:
        target_playlist = sp.album_tracks(playlist_url)
        playlist_name = sp.album(playlist_url)["name"]
        items = target_playlist["items"]
        for count in range(len(items)):
            id_dict["playlist tracks"][items[count]["name"]] = items[count]["id"]
    return playlist_name, id_dict

def run_pull_song(track_url, playlist_url):
    #authorise
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                                   client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                                   redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
                                                   scope="user-library-read"))

    # Build query string for audio feature extraction later
    # Start with target track, then append playlist tracks
    id_dict = {"target" : {}, "playlist tracks" : {}}

    track_name, id_dict = pull_target_track(sp, id_dict, track_url)
    playlist_name, results = pull_playlist(sp, id_dict, playlist_url)

    ids = [value for d in id_dict.values() for value in d.values()]

    #Parcelling out the track IDs into 5s and also formatting so they are accepted by audio feature extraction API
    pcls = {}
    index = 0
    parcel = f""
    count = 0
    for id in range(len(ids)):
        parcel += f"{ids[id]},"
        count += 1
        #don't want this to trigger at the end of a sequence divisible by 5,
        #that would create an empty parcel and error, so add the != check
        if count == 5 and id != len(ids)-1:
            #slice off the comma at the end
            pcls[index] = parcel[:-1]
            #incrementing
            index += 1
            #reset parcel
            parcel = ""
            count = 0
        if id == len(ids):
            pcls[index] = parcel[:-1]
        else:
            pcls[index] = parcel[:-1]

    #Now start pulling audio features
    url = "https://spotify-extended-audio-features-api.p.rapidapi.com/v1/audio-features"
    headers = {
        "x-rapidapi-key": os.environ["RAPID_API_KEY"],
        "x-rapidapi-host": os.environ["RAPID_API_HOST"],
        "Content-Type": "application/json"}

    #Query string has been built, named ids
    #Loop through for each parcel to get all audio features and add results to list
    audios = []
    for parcel in range(len(pcls.values())):
        querystring = {"ids" : f"{pcls[parcel]}"}
        # response = (requests.get(url, headers=headers, params=querystring)).json()
        # audios.extend(response['audio_features'])

    #this block is to replace having to pull data each time since there are usage limits
    #the message reminds me I'm not getting the data I request by URL
    print("TEST MODE - URL AUDIO DATA IS NOT RETRIEVED")
    audios = [{'acousticness': 0.23, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/1qVQIlH6SyNDzNson7ZRy9', 'danceability': 0.467, 'duration_ms': 212573, 'energy': 0.485, 'id': '1qVQIlH6SyNDzNson7ZRy9', 'instrumentalness': 3.5e-06, 'key': 5, 'liveness': 0.0934, 'loudness': -8.706, 'mode': 1, 'speechiness': 0.035, 'tempo': 83.515, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/1qVQIlH6SyNDzNson7ZRy9', 'type': 'audio_features', 'uri': 'spotify:track:1qVQIlH6SyNDzNson7ZRy9', 'valence': 0.193}, {'acousticness': 0.263, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/6dti5eXjL9FxAZyETT5NEj', 'danceability': 0.607, 'duration_ms': 221973, 'energy': 0.85, 'id': '6dti5eXjL9FxAZyETT5NEj', 'instrumentalness': 0.00578, 'key': 8, 'liveness': 0.144, 'loudness': -5.989, 'mode': 1, 'speechiness': 0.0599, 'tempo': 105.025, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/6dti5eXjL9FxAZyETT5NEj', 'type': 'audio_features', 'uri': 'spotify:track:6dti5eXjL9FxAZyETT5NEj', 'valence': 0.559}, {'acousticness': 0.645, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2RFs9C6OfM6MaGBphZi3MB', 'danceability': 0.714, 'duration_ms': 222013, 'energy': 0.651, 'id': '2RFs9C6OfM6MaGBphZi3MB', 'instrumentalness': 2.61e-05, 'key': 2, 'liveness': 0.112, 'loudness': -7.862, 'mode': 0, 'speechiness': 0.0338, 'tempo': 106.973, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2RFs9C6OfM6MaGBphZi3MB', 'type': 'audio_features', 'uri': 'spotify:track:2RFs9C6OfM6MaGBphZi3MB', 'valence': 0.215}, {'acousticness': 0.103, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2gYj9lubBorOPIVWsTXugG', 'danceability': 0.68, 'duration_ms': 176973, 'energy': 0.922, 'id': '2gYj9lubBorOPIVWsTXugG', 'instrumentalness': 0.0, 'key': 0, 'liveness': 0.0877, 'loudness': -1.215, 'mode': 1, 'speechiness': 0.121, 'tempo': 125.014, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2gYj9lubBorOPIVWsTXugG', 'type': 'audio_features', 'uri': 'spotify:track:2gYj9lubBorOPIVWsTXugG', 'valence': 0.799}, {'acousticness': 0.0, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/37bZGx53B90Kv0ftpFDbDZ', 'danceability': 0.6, 'duration_ms': 252000, 'energy': 0.84, 'id': '37bZGx53B90Kv0ftpFDbDZ', 'instrumentalness': 0.0, 'key': 7, 'liveness': 0.09, 'loudness': -3.96, 'mode': 1, 'speechiness': 0.03, 'tempo': 112.99, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/37bZGx53B90Kv0ftpFDbDZ', 'type': 'audio_features', 'uri': 'spotify:track:37bZGx53B90Kv0ftpFDbDZ', 'valence': 0.28}]
    print(f"track name is\n{track_name}, playlist name is\n{playlist_name}, id dict is\n{id_dict}")
    return id_dict, audios