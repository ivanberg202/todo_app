from fastapi import FastAPI, Request, Depends, HTTPException, status, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from fastapi.staticfiles import StaticFiles
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from todoapp3.routers.auth import get_current_user  # Assuming you have this utility function for user authentication
from jose import JWTError, jwt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Set up templates directory
templates = Jinja2Templates(directory="todoapp3/templates")

# Route to handle the dashboard after user login
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: dict = Depends(get_current_user)):
    # If user is not authenticated, redirect them to the login page
    if not current_user:
        return RedirectResponse(url="/login-page", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})

# Mount the static files
app.mount("/static", StaticFiles(directory="todoapp3/static"), name="static")

# Create all database tables
Base.metadata.create_all(bind=engine)

# Health check endpoint
@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


from fastapi.responses import RedirectResponse


# Define a function to serve dashboard.html when root path is accessed
@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """
    Function to serve the dashboard.html template when the root path is accessed.

    Args:
        request (Request): The incoming HTTP request object.

    Returns:
        TemplateResponse: The rendered HTML response for the dashboard page.
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Include existing routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
