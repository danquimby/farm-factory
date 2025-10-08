from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from starlette import status

from app.core.schemas import Token
from app.features.dependencies import get_user_service
from app.services.user_service import UserService

router = APIRouter(prefix="", tags=["core"])


@router.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
    user_service: Annotated[UserService, Depends(get_user_service)],
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    if user := await user_service.authenticate_user(form_data.username, form_data.password):
        if user.refresh_tokens:
            # отдаем последний токен
            result = user.refresh_tokens[-1]
            return {"access_token": result.token, "token_type": ""}
    logger.debug(f'error auth username:{form_data.username} password:{form_data.password}')
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
