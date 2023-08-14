from fastapi import Depends

from lessons.services import LessonService
from utils.unit_of_work import UnitOfWorkBase, UnitOfWork


async def get_lesson_service(uow: UnitOfWorkBase = Depends(UnitOfWork)):
    return LessonService(uow)
