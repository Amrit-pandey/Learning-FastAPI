from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict]= [
  {
    "id": 1,
    "title": "FastAPI is Awesome",
    "content": "FastAPI is a great framework for python, building highly and scalable web APIs.",
    "author": "Corey Schafer",
    "date_posted": "11 July 2026"
  },
  {
    "id": 2,
    "title": "Python is a Great programming language for biginners",
    "content": "Python is a Great programming language for biginners, and FastAPI makes it even better.",
    "author": "Amrit Pandey",
    "date_posted": "12 July 2026"
  },
]
# Frontend Navigation Routes

@app.get("/", include_in_schema=False, name='home')
@app.get("/posts", include_in_schema=False, name='posts')
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get('/posts/{post_id}')
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": "Post"})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

@app.get('/posts/{post_id}')
def error_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(request, "error.html")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

# API ROUTES

@app.get('/api/posts')
def get_posts():
    return posts

@app.get('/api/posts/{post_id}')
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")