from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from ..database import get_db
from ..models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


db_dependency = Annotated[Session, Depends(get_db)]


templates = Jinja2Templates(directory="todoapp3/templates")


### Pages ###

# Route to display the login page
@router.get("/login-page", response_class=HTMLResponse, name="login-page")
async def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Route to display the registration page
@router.get("/register", response_class=HTMLResponse, name="register")
async def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Route to display the post-login dashboard
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


### Endpoints ###

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", status_code=status.HTTP_201_CREATED, name="create_user")
async def create_user(
    db: db_dependency,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(None),
    first_name: str = Form(None),
    last_name: str = Form(None),
    role: str = Form(None),
    phone_number: str = Form(None)
):
    create_user_model = Users(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        role=role,
        hashed_password=bcrypt_context.hash(password),
        is_active=True,
        phone_number=phone_number
    )

    db.add(create_user_model)
    db.commit()

    return {"message": "User registered successfully."}



async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


@router.get("/me", name="get_current_user_info")
async def get_current_user_info(current_user: Annotated[dict, Depends(get_current_user)], db: db_dependency):
    # Fetch the full user data from the database using the user_id from the token
    user = db.query(Users).filter(Users.id == current_user['id']).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Return all user details
    return {
        "username": user.username,
        "user_id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "phone_number": user.phone_number,
        "is_active": user.is_active,
        "phone_number_last_changed": user.phone_number_last_changed
    }


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=15))

    return {'access_token': token, 'token_type': 'bearer'}







