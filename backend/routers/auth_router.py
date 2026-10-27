"""
auth_router.py
-----------------------------------
WATT LINK Authentication Router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import (
    UserCreate,
    UserLogin,
    ChangePassword,
    UserResponse,
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ======================================================
# Register
# ======================================================

@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(

        full_name=user.full_name,

        email=user.email,

        password=hash_password(user.password),

        phone=user.phone,

        residence_id=user.residence_id,

        role="Resident"

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# ======================================================
# Login
# ======================================================

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if db_user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token(
        {
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {

        "access_token": token,

        "token_type": "bearer",

        "user": {

            "id": db_user.id,

            "name": db_user.full_name,

            "email": db_user.email,

            "role": db_user.role

        }

    }


# ======================================================
# Current User
# ======================================================

@router.get("/me", response_model=UserResponse)
def me(
    current_user: User = Depends(get_current_user)
):

    return current_user


# ======================================================
# Change Password
# ======================================================

@router.put("/change-password")
def change_password(

    data: ChangePassword,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    if not verify_password(

        data.old_password,

        current_user.password

    ):

        raise HTTPException(

            status_code=400,

            detail="Old password incorrect"

        )

    current_user.password = hash_password(

        data.new_password

    )

    db.commit()

    return {

        "message": "Password changed successfully"

    }


# ======================================================
# Delete Account
# ======================================================

@router.delete("/delete")
def delete_account(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    db.delete(current_user)

    db.commit()

    return {

        "message": "Account deleted successfully"

    }