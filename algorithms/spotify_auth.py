# ENTIRE FILE IS ARCHIVED NOW, ONLY USED FOR TESTING
#
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
# 
# import os
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())
# #
# # # authorise
# #
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
#
# sp = spotify_auth()
# print(sp.current_user()["images"][0]["url"])

# {'account_id': '4OfKNTjBr1', 'country': 'CA', 'display_name': "Qu'une fraise", 'explicit_content': {'filter_enabled': False, 'filter_locked': False}, 'external_urls': {'spotify': 'https://open.spotify.com/user/z6xkuzga58ybfr60k8adagv1x'}, 'followers': {'href': None, 'total': 3}, 'href': 'https://api.spotify.com/v1/users/z6xkuzga58ybfr60k8adagv1x', 'id': 'z6xkuzga58ybfr60k8adagv1x', 'images': [{'height': 300, 'url': 'https://i.scdn.co/image/ab6775700000ee85a051911474c56374e3859efc', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/ab67757000003b82a051911474c56374e3859efc', 'width': 64}], 'product': 'premium', 'type': 'user', 'uri': 'spotify:user:z6xkuzga58ybfr60k8adagv1x'}