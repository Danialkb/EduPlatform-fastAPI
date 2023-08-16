from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from course_modules.services import CourseModuleService
from database import get_session
from utils.unit_of_work import UnitOfWork


async def get_course_module_service(session: AsyncSession = Depends(get_session)):
    uow = UnitOfWork(session)
    return CourseModuleService(uow)
