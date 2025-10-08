from pydantic import BaseModel


class UserMixin(BaseModel):
    user_id: int | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
