from typing import Annotated, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from ..models import Todos
from ..database import SessionLocal, get_db
from .auth import get_current_user


router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3, max_length=100)
    priority: Optional[int] = Field(None, gt=0, lt=6)
    complete: Optional[bool] = None


def get_todo_or_404(db: Session, user_id: int, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
    return todo_model



# test function created
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

# test functions created
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = get_todo_or_404(db, user.get('id'), todo_id)
    return todo_model

# test function created
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)  # Refresh to get the auto-generated fields like id

    return todo_model


# test function needs update
@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_update: TodoUpdate,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = get_todo_or_404(db, user.get('id'), todo_id)

    # Only update fields that are provided
    if todo_update.title is not None:
        todo_model.title = todo_update.title
    if todo_update.description is not None:
        todo_model.description = todo_update.description
    if todo_update.priority is not None:
        todo_model.priority = todo_update.priority
    if todo_update.complete is not None:
        todo_model.complete = todo_update.complete

    db.commit()
    db.refresh(todo_model)
    return todo_model


# test functions created
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = get_todo_or_404(db, user.get('id'), todo_id)
    db.delete(todo_model)
    db.commit()