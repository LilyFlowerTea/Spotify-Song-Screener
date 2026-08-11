import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="7a13b6abf1aa4079a6fba063710f13a7",
                                                           client_secret="3abc4315a7fe4184b1f1ea7964a25e3b"))
cdp_uri = 'spotify:artist:2eRNMtoi82UZUuaL6naDjA'

results = sp.artist_albums(cdp_uri, album_type = 'album')
albums = results['items']

while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
