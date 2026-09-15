from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Response
from fastapi.responses import RedirectResponse

from pydantic import BaseModel
from enum import Enum
from urllib.parse import urlencode

import os
import secrets
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

import redis
import requests

from algorithms.pull_data_by_id import ComparisonMethod

app = FastAPI()

#setting this using Pydantic, essentially creates a new meta-object type containing the listed objects
class NameReq(BaseModel):
    target_song_url : str
    comparison_url : str
    method : ComparisonMethod
    weight_array : list

#pointing to the html page that builds the webpage
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# create connection to Redis database, used for login identification
red = redis.from_url(
    os.environ["REDIS_URL"],
    decode_responses=True
)

# initial webpage setup, cookie generation
@app.get("/")
def home(request: Request):
    # check if a cookie is present already, if not generate it
    session_id = request.cookies.get("mysession")
    if session_id is None:
        # generate a cookie for the user session, required to check if the login button should be hidden
        session_id = secrets.token_hex(16)

    # check if there is a valid access token associated with this user session, identified by session_id/cookie
    # note here this architecture is not very robust, it could fail if there is an access token
    # but it has expired. solution would be to retrieve access token info and check validity,
    # but I'm not doing that while there are higher priorities
    if red.get(session_id) in [False, None]:
        should_show_login_button = True
    else:
        should_show_login_button = False

    # build webpage
    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"should_show_login_button" : should_show_login_button}
    )
    # attach cookie to response object, can now be matched later
    response.set_cookie(key="mysession", value=session_id, max_age=86400)

    return response

# create a spotify auth object for public playlist access
def create_public_sp():
    public_sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]
        )
    )
    return public_sp

# create a spotify auth object for user logins, identified by a browser cookie
def create_sp(red_cache):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIFY_CLIENT_ID"],
                                                   client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
                                                   redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
                                                   scope="playlist-read-private",
                                                   open_browser = False,
                                                   cache_handler = red_cache
                                                   ))
    return sp

#step 2 is to redirect to spotify login to generate the access token
@app.get("/cookie_to_spotify")
def login(request : Request):
    cookie = request.cookies.get("mysession")
    red_cache = spotipy.RedisCacheHandler(red, key = cookie)
    sp = create_sp(red_cache)
    spotify_auth_url = sp.auth_manager.get_authorize_url()
    return RedirectResponse(spotify_auth_url)

# step 3 is to get the access token, which should now be stored in
# the Redis database during create_sp()
# access token is used to access private user playlists
@app.get("/callback")
def callback(code, request : Request):
    cookie = request.cookies.get("mysession")
    red_cache = spotipy.RedisCacheHandler(red, key = cookie)
    sp = create_sp(red_cache)
    sp.auth_manager.get_access_token(code)
    return RedirectResponse("/")

#pull algorithm functions
from algorithms.pull_data_by_id import pull_data_by_id
from algorithms.analysis import analysis_output

#this is the output returned to be printed on the webpage
@app.post("/data_request")
def processing(data : NameReq, request : Request):
    # public sp suitable for general access to album and artist data
    sp = create_public_sp()
    # add in a check for whether the comparison object is a playlist
    # all playlists, public or private, require owner login to get items
    # therefore check for access token presence, and redirect if none found
    if "playlist" in data.comparison_url:
        # print("playlist in comparison_url - need private sp to access")
        cookie = request.cookies.get("mysession")
        if cookie is None:
            print("No cookie found")
            return {"message" : "login required"}
        if red.get(cookie) is None:
            print("Access token not found")
            return {"message" : "login required"}
        red_cache = spotipy.RedisCacheHandler(red, key = cookie)
        sp = create_sp(red_cache)
        (target_song_name,
         comparison_name,
         id_dict,
         audios,
         comparison_type) = pull_data_by_id(sp,
                                            data.target_song_url,
                                            data.comparison_url,
                                            data.method)
    # if the comparison is not a playlist, it should be album or artist
    # both of these are publicly accessible
    else:
        (target_song_name,
         comparison_name,
         id_dict,
         audios,
         comparison_type) = pull_data_by_id(sp,
                                            data.target_song_url,
                                            data.comparison_url,
                                            data.method)
    unsorted_data_json, sorted_data_json = analysis_output(id_dict, audios, data.weight_array)
    return {"target_song_name" : f"Your target song is:\n{target_song_name}",
            "comparison_name" : f"Your target comparison is tracks from the {comparison_type}:\n{comparison_name}",
            "distance_data" : unsorted_data_json,
            "sorted_data" : sorted_data_json
            }

# logout function
@app.delete("/logout")
def logout(request: Request):
    cookie = request.cookies.get("mysession")
    red.delete(cookie)
    response = RedirectResponse("/")
    response.delete_cookie("mysession")
    return response

# uvicorn api.index:app --reload --port 1234