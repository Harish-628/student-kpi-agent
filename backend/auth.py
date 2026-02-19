"""
Authentication utilities for JWT token generation and validation.
Provides password hashing and token management.
"""

from datetime import datetime, timedelta
from typing import Optional
import jwt
import hashlib
import hmac

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"  # Change this to a secure random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a password using HMAC-SHA256."""
    return hmac.new(
        SECRET_KEY.encode(),
        password.encode(),
        hashlib.sha256
    ).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hash."""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary with token claims (should include 'sub' for user ID)
        expires_delta: Token expiration time delta
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string
        
    Returns:
        Token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None
    except jwt.ExpiredSignatureError:
        return None


def create_demo_users() -> list:
    """Generate demo users with hashed passwords."""
    demo_users = [
        {
            "id": 1,
            "email": "student@example.com",
            "password_hash": hash_password("student123"),
            "name": "John Student",
            "role": "student",
            "department": "CSE",
            "is_active": True
        },
        {
            "id": 2,
            "email": "faculty@example.com",
            "password_hash": hash_password("faculty123"),
            "name": "Dr. Faculty",
            "role": "faculty",
            "department": "CSE",
            "is_active": True
        },
        {
            "id": 3,
            "email": "coordinator@example.com",
            "password_hash": hash_password("coordinator123"),
            "name": "Coordinator",
            "role": "coordinator",
            "department": "Academic Affairs",
            "is_active": True
        },
        {
            "id": 4,
            "email": "admin@example.com",
            "password_hash": hash_password("admin123"),
            "name": "Admin User",
            "role": "admin",
            "department": "Administration",
            "is_active": True
        }
    ]
    return demo_users
