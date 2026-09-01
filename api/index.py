from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from enum import Enum
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
     id_dict, audios) = pull_data_by_id(data.target_song_url,
                                        data.comparison_url,
                                        data.method)
    unsorted_data_json, sorted_data_json = analysis_output(id_dict, audios)
    return {"target_song_name" : f"Your target song is: {target_song_name}",
            "comparison_name" : f"Your target comparison is: {comparison_name}",
            "distance_data" : unsorted_data_json,
            "sorted_data" : sorted_data_json
            }

# @app.get("/login")
# def auth(client_id : str,
#          response_type : str,
#          redirect_uri : str,
#          state : str,
#          scope : str):

    

# uvicorn api.index:app --reload