from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from users.repository import UserRepo
from users.schemas import UserCreate, ShowUser
from users.services import UserService

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, session: AsyncSession = Depends(get_session)) -> ShowUser:
    user_service = UserService(session)
    return await user_service.create_new_user(body)
