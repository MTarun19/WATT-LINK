"""
dependencies.py
---------------------------------------
WATT LINK Common Dependencies
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from auth import get_current_user
from models import User


# =====================================================
# Database Dependency
# =====================================================

def get_database():

    db = next(get_db())

    try:
        yield db

    finally:
        db.close()


# =====================================================
# Current Logged-in User
# =====================================================

def current_user(
    user: User = Depends(get_current_user)
):

    return user


# =====================================================
# Admin Only Dependency
# =====================================================

def admin_required(
    current: User = Depends(get_current_user)
):

    if current.role != "Admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required."
        )

    return current


# =====================================================
# Resident Only Dependency
# =====================================================

def resident_required(
    current: User = Depends(get_current_user)
):

    if current.role not in ["Resident", "Admin"]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resident access required."
        )

    return current


# =====================================================
# AI Manager Access
# =====================================================

def ai_manager_access(
    current: User = Depends(get_current_user)
):

    if current.role not in ["Admin", "AI Manager"]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="AI Manager access denied."
        )

    return current


# =====================================================
# Marketplace Access
# =====================================================

def marketplace_access(
    current: User = Depends(get_current_user)
):

    if current.role not in ["Resident", "Admin"]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Marketplace access denied."
        )

    return current


# =====================================================
# Sensor Access
# =====================================================

def sensor_access(
    current: User = Depends(get_current_user)
):

    return current


# =====================================================
# Relay Access
# =====================================================

def relay_access(
    current: User = Depends(get_current_user)
):

    if current.role not in ["Admin", "Resident"]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Relay control denied."
        )

    return current


# =====================================================
# Battery Access
# =====================================================

def battery_access(
    current: User = Depends(get_current_user)
):

    return current