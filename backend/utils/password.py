"""
password.py
---------------------------------------
Password Utilities for WATT LINK
"""

import re
import secrets
import string

from passlib.context import CryptContext

# ============================================================
# Password Hashing Configuration
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ============================================================
# Hash Password
# ============================================================

def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    """
    return pwd_context.hash(password)


# ============================================================
# Verify Password
# ============================================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Compare plain password with hashed password.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# Password Strength Validation
# ============================================================

def validate_password(password: str):

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    return True, "Password is strong."


# ============================================================
# Generate Secure Password
# ============================================================

def generate_password(length: int = 12):

    characters = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*"
    )

    while True:

        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        valid, _ = validate_password(password)

        if valid:
            return password


# ============================================================
# Password Strength Score
# ============================================================

def password_strength(password: str):

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    levels = {
        1: "Very Weak",
        2: "Weak",
        3: "Medium",
        4: "Strong",
        5: "Very Strong"
    }

    return {
        "score": score,
        "strength": levels.get(score, "Very Weak")
    }