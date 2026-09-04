# ENTIRE FILE IS ARCHIVED NOW, ONLY USED FOR TESTING

# import spotipy
# from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
#
# import os
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())
#
# # authorise
#
# def spotify_auth():
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIFY_CLIENT_ID"],
#                                                    client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
#                                                    redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
#                                                    scope="playlist-read-private",
#                                                    open_browser = False,
#                                                    # cache_handler =
#                                                    ))
#     return sp
#
# def spotify_client_auth():
#     sp = spotipy.Spotify(
#         auth_manager=SpotifyClientCredentials(
#             client_id=os.environ["SPOTIFY_CLIENT_ID"],
#             client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
#         )
#     )
#     return sp

# sp = spotify_client_auth()
# print(sp.album("https://open.spotify.com/album/3B4cg0LWmS1RCUJdOZ1aJ6"))