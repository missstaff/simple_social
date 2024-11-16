from database import get_post, insert_post
from models import Post, Posts, UserPost
from sqlite3 import Connection, Row
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import sqlite3

app = FastAPI()

# Establish database connection
connection = sqlite3.connect('social.db')
connection.row_factory = sqlite3.Row

templates = Jinja2Templates(directory="./templates")
user_id = 1

@app.get("/home")
async def home(request: Request) -> HTMLResponse:
    posts = get_post(connection).posts  

    # context = {
    #    "request": request,
    #    "posts" : [
    #           {"post_title": "Pydantic", "post_text": "Test Text", "user_id": 2},
    #           {"post_title": "PydanticII", "post_text": "Test Text", "user_id": 2}
    #    ]
    # }
    
    context = {
        "request": request,
        "posts": get_post(connection).posts
    }
    return templates.TemplateResponse("./index.html", context=context)

@app.get("/posts")
async def posts(request: Request) -> HTMLResponse:
    posts = get_post(connection)
    return templates.TemplateResponse("./posts.html", context={"request": request, "posts": posts.posts})

@app.post("/post")
async def add_post(post: UserPost, request: Request) -> HTMLResponse:
    post =(Post(user_id=user_id, **post.model_dump()))
    insert_post(connection, post)
    posts = get_post(connection)
    return templates.TemplateResponse("./posts.html", context={"request": request, "posts": posts})
