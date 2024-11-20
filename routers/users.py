from typing import Annotated, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from ..models import Users, PhoneNumberHistory
from ..database import get_db
from .auth import get_current_user
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

router = APIRouter(
    prefix='/user',
    tags=['user']
)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class PhoneNumberUpdateRequest(BaseModel):
    phone_number: str


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    phone_number: Optional[str] = None


# Define Berlin timezone offset manually (adjust for DST as needed)
BERLIN_TIMEZONE = timezone(timedelta(hours=1))  # Adjust to +2 for DST if applicable


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    # Convert phone_number_last_changed to Berlin time if it exists
    if user_model and user_model.phone_number_last_changed:
        user_model.phone_number_last_changed = user_model.phone_number_last_changed.astimezone(BERLIN_TIMEZONE)

    return user_model


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()



@router.put("/phone_number", status_code=200)
async def update_phone_number(
    user: user_dependency, db: db_dependency, new_phone_number: str
):
    # Fetch the user model
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Save the previous phone number to the PhoneNumberHistory table
    phone_history = PhoneNumberHistory(
        user_id=user_model.id,
        phone_number=user_model.phone_number,  # Save the previous number
        changed_at=datetime.now(timezone.utc)
    )
    db.add(phone_history)

    # Update the phone number
    user_model.phone_number = new_phone_number
    user_model.phone_number_last_changed = datetime.now(timezone.utc)

    # Commit the changes to the database
    db.add(user_model)
    db.commit()
    db.refresh(user_model)  # Refresh to get the updated user

    return {"message": "Phone number updated successfully"}


@router.get("/phone_number/history", status_code=200)
async def get_phone_number_history(user: user_dependency, db: db_dependency):
    # Fetch the phone number history for the user
    phone_history = db.query(PhoneNumberHistory).filter(PhoneNumberHistory.user_id == user.get('id')).all()

    if not phone_history:
        raise HTTPException(status_code=404, detail="No phone number history found")

    return phone_history


@router.put("/update_details", status_code=200)
async def update_user_details(
        current_user: user_dependency,
        user_update: UserUpdateRequest,
        db: Session = Depends(get_db),
        user_identifier: Optional[str] = Query(
            None,  # Optional parameter for non-admins
            description="Username or email of the user to update (required for admins)"
        )
):
    # Logic to determine which user to update
    if current_user.get('user_role') == 'admin':
        # Admins must provide a user_identifier
        if not user_identifier:
            raise HTTPException(status_code=400, detail="Admin must provide a username or email to update a user.")

        # Fetch the target user by username or email
        user_model = db.query(Users).filter(
            (Users.username == user_identifier) | (Users.email == user_identifier)
        ).first()

        if user_model is None:
            raise HTTPException(status_code=404, detail="User not found")

    else:
        # Non-admin users are only allowed to update their own details
        if user_identifier:
            raise HTTPException(status_code=403, detail="Non-admin users cannot specify another user.")

        # Update the current user's own details
        user_model = db.query(Users).filter(Users.id == current_user.get('id')).first()

        if user_model is None:
            raise HTTPException(status_code=404, detail="User not found")

    # Update user details if provided
    if user_update.username is not None:
        # Check for username uniqueness
        username_check = db.query(Users).filter(Users.username == user_update.username).first()
        if username_check:
            if username_check.id != user_model.id:
                raise HTTPException(status_code=400, detail="Username is already in use by another account")
        user_model.username = user_update.username

    if user_update.email is not None:
        # Check for email uniqueness
        email_check = db.query(Users).filter(Users.email == user_update.email).first()
        if email_check:
            if email_check.id != user_model.id:
                raise HTTPException(status_code=400, detail="Email is already in use by another account")
        user_model.email = user_update.email

    if user_update.first_name is not None:
        user_model.first_name = user_update.first_name
    if user_update.last_name is not None:
        user_model.last_name = user_update.last_name

    # Only admins can change roles
    if user_update.role is not None:
        if current_user.get('user_role') != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can change the role")
        user_model.role = user_update.role

    if user_update.phone_number is not None:
        user_model.phone_number = user_update.phone_number

    # Commit changes to the database
    db.commit()

    # Optional: refresh the instance to return the latest state
    db.refresh(user_model)

    return {"message": "User details updated successfully", "user": user_model}
