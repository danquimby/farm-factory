from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.security import create_access_token
from app.features.auth.models import User
from app.features.auth.schemas import (
    Token,
    UserRegister,
    UserResponse,
)
from app.features.dependencies import get_current_user, get_user_service
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user: UserRegister, user_service: Annotated[UserService, Depends(get_user_service)]
):
    if await user_service.exist_user_by_email(str(user.email)):
        raise HTTPException(status_code=400, detail="Email already registered")
    if await user_service.exist_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = await user_service.create_user(user)
    return UserResponse.model_validate(db_user)


@router.post("/login", response_model=Token)
async def login(
    user_service: Annotated[UserService, Depends(get_user_service)],
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = await user_service.create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token.token,
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str, db: AsyncSession = Depends(get_async_session)
):
    pass
    # user = verify_refresh_token(db, refresh_token)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
    #     )
    #
    # # Create new tokens
    # access_token = create_access_token(data={"sub": user.email})
    # new_refresh_token = create_refresh_token(db, user.id)
    #
    # # Revoke old refresh token
    # revoke_refresh_token(db, refresh_token)
    #
    # return {
    #     "access_token": access_token,
    #     "token_type": "bearer",
    #     "refresh_token": new_refresh_token,
    # }


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
