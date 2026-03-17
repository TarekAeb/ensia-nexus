# test hash functions
import pytest
from app.core.security import hash_password, verify_password


def test_hash_and_verify_password():
    password = "SecurePassword123!"
    hashed = hash_password(password)
    assert isinstance(hashed, bytes)
    assert verify_password(password, hashed) == True
    assert verify_password("WrongPassword", hashed) == False


def test_hash_password_invalid_input():
    with pytest.raises(ValueError):
        hash_password("")
    with pytest.raises(ValueError):
        hash_password(12345)  # Not a string


def test_verify_password_invalid_input():
    hashed = hash_password("ValidPassword")
    with pytest.raises(ValueError):
        verify_password("", hashed)
    with pytest.raises(ValueError):
        verify_password(12345, hashed)  # Not a string
    with pytest.raises(ValueError):
        verify_password("ValidPassword", "NotBytes")  # Hashed password not bytes

# To run these tests, use the command: pytest tests/hash_test.py
