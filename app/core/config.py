import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class RedisConfig(BaseModel):
    user: str | None = None
    password: str | None = None
    port: int = 6370
    host: str = "localhost"
    db: str = "0"

    @property
    def url(self) -> str:
        if self.user and self.password:
            return (
                f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
            )
        return f"redis://{self.host}:{self.port}/{self.db}"

    @property
    def psub(self):
        return f"__keyevent@{self.db}__:expired"


class DataBaseSetting(BaseModel):
    host: str
    user: str
    port: int = 5432
    password: str
    name: str = "farm-db"
    test_name: str | None = "test-farm-db"

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def test_db_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.test_name}"


class SecuritySettings(BaseModel):
    refresh_token_expire_days: int | None = 5
    access_token_expire_minutes: int | None = 60 * 60
    secret_key: str | None = "secret_key"
    algorithm: str | None = "HS256"


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 7000

    security: SecuritySettings = SecuritySettings()
    redis: RedisConfig
    db: DataBaseSetting

    model_config = SettingsConfigDict(
        env_file=(".env.dev", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
    )


settings: Settings = Settings()
