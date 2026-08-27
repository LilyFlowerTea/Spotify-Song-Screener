from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#setting this using Pydantic, essentially creates a new meta-object type containing the listed objects
class NameReq(BaseModel):
    target_song_url : str
    # playlist_url : str

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

#this is the output returned to be printed on the webpage
@app.post("/analysis")
def analysis(data : NameReq):
    return {"target_song_url" : f"Your target song is {data.target_song_url}"
        # ,"playlist_url" : f"Your target playlist is {data.playlist_url}"
            }

# uvicorn app.main:app --reload