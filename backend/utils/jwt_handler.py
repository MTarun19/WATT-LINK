"""
jwt_handler.py
---------------------------------------
JWT Authentication Handler
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

# ============================================================
# Configuration
# ============================================================

SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ============================================================
# Create Access Token
# ============================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):

    payload = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload.update({"exp": expire})

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ============================================================
# Decode Token
# ============================================================

def decode_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


# ============================================================
# Verify Token
# ============================================================

def verify_token(token: str):

    payload = decode_token(token)

    if payload is None:
        return False

    return True


# ============================================================
# Extract User Email
# ============================================================

def get_email(token: str):

    payload = decode_token(token)

    if payload is None:
        return None

    return payload.get("sub")


# ============================================================
# Extract User Role
# ============================================================

def get_role(token: str):

    payload = decode_token(token)

    if payload is None:
        return None

    return payload.get("role")