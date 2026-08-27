from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#setting this using Pydantic, not entirely sure how this works
class NameReq(BaseModel):
    name : str

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
@app.post("/hello")
def greet(data : NameReq):
    return {"message" : f"Sup {data.name}"}

# uvicorn app.main:app --reload