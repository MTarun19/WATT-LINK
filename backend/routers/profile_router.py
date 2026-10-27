"""
profile_router.py
-----------------------------------
WATT LINK Profile Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import ProfileUpdate, UserResponse
from auth import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/", response_model=UserResponse)
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.put("/update", response_model=UserResponse)
def update_profile(
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if profile.full_name is not None:
        current_user.full_name = profile.full_name

    if profile.phone is not None:
        current_user.phone = profile.phone

    if profile.email is not None:
        current_user.email = profile.email

    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete("/delete")
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db.delete(current_user)
    db.commit()

    return {
        "message": "Profile deleted successfully."
    }