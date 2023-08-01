from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from users.schemas import UserCreate, ShowUser, Token, UserAuth
from users.services import UserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, session: AsyncSession = Depends(get_session)) -> ShowUser:
    user_service = UserService(session)
    return await user_service.create_new_user(body)


@router.post("/login/", response_model=Token)
async def authenticate(body: UserAuth, session: AsyncSession = Depends(get_session)):
    user_service = UserService(session)
    return await user_service.verify_user(body)
