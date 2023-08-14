from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from courses.services import CourseService
from database import get_session
from utils.unit_of_work import UnitOfWork


async def get_course_service(session: AsyncSession = Depends(get_session)):
    uow = UnitOfWork(session)
    return CourseService(uow)
