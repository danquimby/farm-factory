from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.base_repository import BaseRepository
from app.features.auth.models import User, RefreshToken


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, db: AsyncSession):
        super().__init__(RefreshToken, db)

    async def verify_refresh_token(self, token: str) -> User | None:
        query = (
            select(RefreshToken)
            .where(RefreshToken.token == token)
            .options(selectinload(RefreshToken.user))
        )
        result = await self.db.execute(query)
        # todo пока уберу время жизни токена
        # if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        #     return None

        if db_token := result.scalar_one_or_none():
            return db_token.user



class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_user_by_email(self, email: str) -> User | None:
        query = (
            select(User)
            .where(User.email == email)
            .options(selectinload(User.refresh_tokens))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        query = (
            select(User)
            .where(User.username == username)
            .options(selectinload(User.refresh_tokens))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

