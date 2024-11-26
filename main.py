from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models import Base
from database import engine
from routers import auth, todos, admin, users
import logging
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Set up templates directory
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

print(f"Templates directory: {os.path.join(BASE_DIR, 'templates')}")

# Mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create all database tables
Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("/static/favicon.ico")


# Include existing routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
