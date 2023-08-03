from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from users.schemas import UserCreate, ShowUser, Token, UserAuth
from users.services import UserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, session: AsyncSession = Depends(get_session)) -> ShowUser:
    user_service = UserService(session)
    return await user_service.create_new_user(body)


@router.post("/token/", response_model=Token)
async def authenticate(
        form: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    user_service = UserService(session)
    return await user_service.verify_user(form)


@router.get("/{id}/", response_model=ShowUser)
async def get_user(id: str, session: AsyncSession = Depends(get_session)) -> ShowUser:
    user_service = UserService(session)
    return await user_service.get_user(id)

