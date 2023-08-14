from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from users.dependencies import get_user_service
from users.schemas import UserCreate, ShowUser, Token, UserAuth
from users.services import UserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/", response_model=ShowUser)
async def create_user(
        body: UserCreate,
        user_service: UserService = Depends(get_user_service)
) -> ShowUser:
    return await user_service.create_new_user(body)


@router.post("/token/", response_model=Token)
async def authenticate(
        user_service: UserService = Depends(get_user_service),
        form: OAuth2PasswordRequestForm = Depends(),
):
    return await user_service.verify_user(form)


@router.get("/{id}/", response_model=ShowUser)
async def get_user(
        id: str,
        user_service: UserService = Depends(get_user_service)
) -> ShowUser:
    return await user_service.get_user(id)

