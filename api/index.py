from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from pydantic import BaseModel
from enum import Enum
from urllib.parse import urlencode

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import redis
import requests

from algorithms.pull_data_by_id import ComparisonMethod

app = FastAPI()

#setting this using Pydantic, essentially creates a new meta-object type containing the listed objects
class NameReq(BaseModel):
    target_song_url : str
    comparison_url : str
    method : ComparisonMethod

#pointing to the html page that builds the webpage
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

#build webpage
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

#pull algorithm functions
from algorithms.pull_data_by_id import pull_data_by_id
from algorithms.analysis import analysis_output

#this is the output returned to be printed on the webpage
@app.post("/data_request")
def processing(data : NameReq):
    (target_song_name,
     comparison_name,
     id_dict,
     audios,
     comparison_type) = pull_data_by_id(data.target_song_url,
                                        data.comparison_url,
                                        data.method)
    unsorted_data_json, sorted_data_json = analysis_output(id_dict, audios)
    return {"target_song_name" : f"Your target song is: {target_song_name}",
            "comparison_name" : f"Your target comparison is tracks from the {comparison_type}: {comparison_name}",
            "distance_data" : unsorted_data_json,
            "sorted_data" : sorted_data_json
            }


red = redis.from_url(
    os.environ["REDIS_URL"],
    decode_responses=True
)
red_cache = spotipy.RedisCacheHandler(red, key = "test_id")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                                   client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                                   redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
                                                   scope="playlist-read-private",
                                                   open_browser = False,
                                                   cache_handler = red_cache
                                                   ))

@app.get("/login")
def login():


@app.get("/callback")
def callback(code, state):



# uvicorn api.index:app --reload --port 1234