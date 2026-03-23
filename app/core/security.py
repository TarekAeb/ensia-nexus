from datetime import datetime, timedelta
import bcrypt
from jose import jwt, JWTError
from fastapi import HTTPException

# use environment variables
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def token_generator(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def decode_token(token: str):
    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(401, "Invalid token")

        return int(user_id)

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
