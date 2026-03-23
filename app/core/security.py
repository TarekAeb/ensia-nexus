from datetime import datetime, timedelta
import bcrypt
from jose import jwt, JWTError
from fastapi import HTTPException

# use environment variables
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def _create_token(user_id: int, expires_delta: timedelta, token_type: str):
    expire = datetime.utcnow() + expires_delta

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": token_type
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_tokens(user_id: int, REFRESH_TOKEN_EXPIRE_DAYS=60 * 60 * 24 * 7):
    access_token = _create_token(
        user_id,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "access"
    )

    refresh_token = _create_token(
        user_id,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "refresh"
    )

    return access_token, refresh_token


def decode_token(token: str):
    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(401, "Invalid or expired token")


def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    Returns the hashed password as bytes.
    """
    if not isinstance(plain_password, str) or not plain_password:
        raise ValueError("Password must be a non-empty string.")

    # Convert to bytes
    password_bytes = plain_password.encode('utf-8')

    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: bytes | str) -> bool:
    """
    Verify a plain text password against a hashed password.
    Returns True if match, False otherwise.
    """

    if not isinstance(plain_password, str) or not plain_password:
        raise ValueError("Password must be a non-empty string.")
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    if not isinstance(hashed_password, bytes):
        raise ValueError("Hashed password must be bytes.")

    password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)
