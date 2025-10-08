from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets
import string

from settings import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT tokens
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.security.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.security.secret_key, algorithm=settings.security.algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.security.secret_key,
            algorithms=[settings.security.algorithm],
        )
        return payload
    except JWTError:
        return {}


def generate_random_password(length: int = 12) -> str:
    """
    Generate a random password with letters, digits, and special characters.
    """
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(characters) for _ in range(length))


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    """
    return secrets.token_urlsafe(length)


def validate_password_strength(password: str) -> bool:
    """
    Validate password strength.
    Minimum 8 characters, at least one uppercase, one lowercase, one digit, one special character.
    """
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*" for char in password):
        return False
    return True
