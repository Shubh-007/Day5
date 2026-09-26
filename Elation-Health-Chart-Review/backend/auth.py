"""Authentication, authorization, and RBAC utilities."""

import os
import json
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, Header
from pydantic import BaseModel


# Password hasher (argon2)
ph = PasswordHasher()


class UserRecord:
    """Internal user record loaded from users.json"""
    def __init__(self, username: str, password_hash: str, role: str, display_name: str):
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.display_name = display_name


class CurrentUser(BaseModel):
    """Current authenticated user context."""
    username: str
    role: str
    name: str  # display_name (used for RBAC matching against primaryCareProvider)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "schen",
                "role": "clinician",
                "name": "Dr. Sarah Chen"
            }
        }


# Load users from JSON on module import
USERS: dict[str, UserRecord] = {}

def _load_users():
    """Load user records from backend/data/users.json"""
    global USERS
    users_file = os.path.join(os.path.dirname(__file__), "data", "users.json")
    if not os.path.exists(users_file):
        # If users.json doesn't exist, return empty (will cause login to fail)
        return

    with open(users_file, "r") as f:
        data = json.load(f)

    for user_data in data.get("users", []):
        username = user_data["username"]
        USERS[username] = UserRecord(
            username=username,
            password_hash=user_data["password_hash"],
            role=user_data["role"],
            display_name=user_data["display_name"]
        )


_load_users()


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2."""
    return ph.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a hash."""
    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False


def authenticate_user(username: str, password: str) -> Optional[UserRecord]:
    """Authenticate a user by username/password. Returns UserRecord or None."""
    user = USERS.get(username)
    if user and verify_password(password, user.password_hash):
        return user
    return None


def create_access_token(username: str, role: str, display_name: str, expires_minutes: Optional[int] = None) -> str:
    """
    Create a JWT access token.

    Args:
        username: User's username
        role: User's role (admin, clinician)
        display_name: User's display name (used for RBAC)
        expires_minutes: Token expiry time in minutes (from env, default 60)

    Returns:
        JWT token string
    """
    if expires_minutes is None:
        expires_minutes = int(os.environ.get("JWT_EXPIRY_MINUTES", "60"))

    secret_key = os.environ.get("JWT_SECRET_KEY")
    if not secret_key:
        raise ValueError(
            "JWT_SECRET_KEY environment variable is not set. "
            "Generate one with: python3 -c 'import secrets; print(secrets.token_urlsafe(32))'"
        )

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)

    payload = {
        "sub": username,
        "role": role,
        "name": display_name,
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.

    Returns:
        Decoded token payload

    Raises:
        jwt.InvalidTokenError: If token is invalid, expired, or signature doesn't match
    """
    secret_key = os.environ.get("JWT_SECRET_KEY")
    if not secret_key:
        raise ValueError("JWT_SECRET_KEY environment variable is not set")

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.InvalidTokenError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise e


async def get_current_user(authorization: Optional[str] = Header(None)) -> CurrentUser:
    """
    FastAPI dependency to extract and verify the current user from the Authorization header.

    Raises:
        HTTPException(401): If token is missing, invalid, or expired
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = parts[1]

    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        role = payload.get("role")
        name = payload.get("name")

        if not all([username, role, name]):
            raise HTTPException(status_code=401, detail="Invalid token claims")

        return CurrentUser(username=username, role=role, name=name)
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def can_access_patient(user: CurrentUser, patient: dict) -> bool:
    """
    Check if a user can access a specific patient's data.

    Rules:
    - Admins can access any patient
    - Clinicians can only access patients where primaryCareProvider matches their name

    Args:
        user: Current user
        patient: Patient record dict with "primaryCareProvider" field

    Returns:
        True if user can access the patient, False otherwise
    """
    if user.role == "admin":
        return True

    if user.role == "clinician":
        primary_care_provider = patient.get("primaryCareProvider", "")
        return primary_care_provider == user.name

    return False
