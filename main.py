from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import CreatePost, PostResponse

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

@app.get('/posts/{post_id}', include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": "Post"})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

# API ROUTES

@app.get('/api/posts', response_model=list[PostResponse])
def get_posts():
    return posts

@app.post('/api/create-post', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost):
    new_id = max(p["id"] for p in posts) + 1  if posts else 1
    new_post = {
        "id": new_id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "date_posted": "July 12, 2026"
    }
    posts.append(new_post)
    return new_post

@app.get('/api/posts/{post_id}', response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )