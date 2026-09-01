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

import random
import string
import requests
import base64

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

def auth_access():
    state = "".join(random.choices(string.ascii_letters + string.digits, k = 16))
    params = {
        "response_type" : "code",
        "client_id" : os.environ["SPOTIPY_CLIENT_ID"],
        "scope" : "playlist-read-private",
        "redirect_uri" : os.environ["SPOTIPY_REDIRECT_URI"],
        "state" : state
    }
    auth_url = "https://accounts.spotify.com/authorize?"+urlencode(params)
    return auth_url

@app.get("/login")
async def login():
    auth_url = auth_access()
    return RedirectResponse(auth_url)

@app.get("/")
def callback(code, state):
    if code == None:
        return
    else:
        client_creds = f"{os.environ["SPOTIPY_CLIENT_ID"]}:{os.environ["SPOTIPY_CLIENT_SECRET"]}"
        client_creds = base64.b64encode(client_creds.encode())
        data = {
            "grant_type" : "authorization_code",
            "code" : code,
            "redirect_uri" : os.environ["SPOTIPY_REDIRECT_URI"]
        }
        headers = {
            "Authorization" : f"Basic {client_creds.decode()}",
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        access_response = requests.post("https://accounts.spotify.com/api/token",
                      data = data,
                      headers = headers
        )
        access_data = access_response.json()
    return access_data["access_token"], access_data["refresh_token"]


# uvicorn api.index:app --reload