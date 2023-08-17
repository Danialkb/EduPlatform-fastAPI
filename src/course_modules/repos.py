from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from starlette import status

from course_modules.models import Module
from lessons.models import Lesson
from utils.repository_base import RepositoryBase


class CourseModuleRepo(RepositoryBase):
    model = Module

    async def list(self, course_id):
        query = select(self.model)\
            .where(self.model.course_id == course_id)\
            .options(selectinload(self.model.lessons))

        result = await self.db_session.execute(query)
        course_modules = result.scalars().all()
        if len(course_modules) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No modules for this course"
            )

        return course_modules
