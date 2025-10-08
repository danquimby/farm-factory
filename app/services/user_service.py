import secrets
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import HTTPException
from app.features.auth.models import User, RefreshToken
from app.features.auth.repository import UserRepository, RefreshTokenRepository
from app.features.auth.schemas import UserRegister, RefreshTokenCreate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name="JWT")


class UserService:
    user_repository: UserRepository
    token_repository: RefreshTokenRepository

    def __init__(
        self, user_repository: UserRepository, token_repository: RefreshTokenRepository
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    async def create_user(self, user: UserRegister) -> User:
        result = await self.user_repository.create(
            UserCreate(
                hashed_password = self.get_password_hash(user.password),
                email=user.email,
                username=user.username
            )
        )
        return result

    async def exist_user_by_email(self, email: str) -> bool:
        try:
            await self.get_user_by_email(email)
            return True
        except:
            return False

    async def exist_user_by_username(self, username: str) -> bool:
        try:
            await self.get_user_by_username(username)
            return True
        except:
            return False

    async def get_user_by_email(self, email: str) -> User | None:
        if user := await self.user_repository.get_user_by_email(email):
            return user
        raise HTTPException(404, f"not found user by {email=}")

    async def get_user_by_username(self, username: str) -> User | None:
        if user := await self.user_repository.get_user_by_username(username):
            return user
        raise HTTPException(404, f"not found user by {username=}")

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.get_user_by_username(username)
        if self.verify_password(password, user.hashed_password):
            return user
        raise HTTPException(404, f"password incorrect")

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                minutes=settings.security.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.security.secret_key,
            algorithm=settings.security.algorithm,
        )
        return encoded_jwt

    async def create_refresh_token(self, user_id: int) -> RefreshToken:

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(
            days=settings.security.refresh_token_expire_days
        )

        return await self.token_repository.create(
            RefreshTokenCreate(user_id=user_id, token=token, expires_at=expires_at)
        )

    async def verify_refresh_token(self, token: str) -> User | None:
        if result := await self.token_repository.verify_refresh_token(token):
            return result
        raise HTTPException(404, f"verify error {token=}")

    async def get_current_user(self, token: str) -> User | None:
        if user := await self.verify_refresh_token(token):
            return user
