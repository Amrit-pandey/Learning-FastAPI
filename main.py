from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

posts: list[dict]= [
  {
    "id": 1,
    "title": "FastAPI is Awesome",
    "content": "FastAPI is a great framework for python, building highly and scalable web APIs.",
    "author": "Corey Schafer"
  },
  {
    "id": 2,
    "title": "Python is a Great programming language for biginners",
    "content": "Python is a Great programming language for biginners, and FastAPI makes it even better.",
    "author": "Amrit Pandey"
  },
]

@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get("/api/posts")
def get_posts():
    return posts