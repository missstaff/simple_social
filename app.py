from database import get_post, insert_post
from models import Post, Posts
from sqlite3 import Connection, Row
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request


app = FastAPI()
connection = Connection('social.db')
connection.row_factory = Row

templates = Jinja2Templates(directory="./templates")

@app.get("/home")
async def home(request : Request)-> HTMLResponse:
    return templates.TemplateResponse("./index.html", context={"request": request})


@app.get("/posts")
async def posts()->Posts:
    return get_post(connection)

@app.post("/posts")
async def post(post: Post)->Post:
    insert_post(connection, post)
    return post