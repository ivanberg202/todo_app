from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
import logging
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse



# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Set up templates directory
templates = Jinja2Templates(directory="todoapp3/templates")


# Mount the static files
app.mount("/static", StaticFiles(directory="todoapp3/static"), name="static")

# Create all database tables
Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("todoapp3/static/favicon.ico")


# Include existing routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
