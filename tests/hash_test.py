# test hash functions
import pytest
from app.core.security import hash_password, verify_password




def test_hash_and_verify_password():
    password = "SecurePassword123!"
    hashed = hash_password(password)

    # now returns string
    assert isinstance(hashed, str)

    # bcrypt hashes always start like this
    assert hashed.startswith("$2b$")

    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


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
        verify_password("ValidPassword", 12345)  # Hashed password not string
