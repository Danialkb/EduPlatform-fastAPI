from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from lessons.services import LessonService
from utils.unit_of_work import UnitOfWork


async def get_lesson_service(session: AsyncSession = Depends(get_session)):
    uow = UnitOfWork(session)
    return LessonService(uow)
