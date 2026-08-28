from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#setting this using Pydantic, essentially creates a new meta-object type containing the listed objects
class NameReq(BaseModel):
    target_song_url : str
    playlist_url : str

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

#pull algorithm function
from .analysis import analysis_output

#this is the output returned to be printed on the webpage
@app.post("/data request")
def processing(data : NameReq):
    target_song_name, playlist_name, unsorted_data_json, sorted_data_json = analysis_output(data.target_song_url, data.playlist_url)
    return {"target_song_url" : f"Your target song is: {target_song_name}",
            "playlist_url" : f"Your target playlist is: {playlist_name}",
            "distance_data" : unsorted_data_json,
            "sorted_data" : sorted_data_json
            }

# uvicorn app.main:app --reload