from fastapi import Depends

from courses.services import CourseService
from utils.unit_of_work import UnitOfWorkBase, UnitOfWork


async def get_course_service(uow: UnitOfWorkBase = Depends(UnitOfWork)):
    return CourseService(uow)
