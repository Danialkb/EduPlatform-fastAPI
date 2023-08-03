from typing import List

from sqlalchemy import select

from courses.models import Course
from courses.schemas import CourseCreate, ShowCourse
from utils.repository_base import RepositoryBase


class CourseRepo(RepositoryBase):

    async def create_course(self, body: CourseCreate, owner_id: str, filename: str) -> Course:
        new_course = Course(
            title=body.title,
            owner_id=owner_id,
            description=body.description,
        )
        if filename:
            new_course.logo = filename
        self.db_session.add(new_course)
        await self.db_session.commit()
        return new_course

    async def get_courses(self):
        query = select(Course)
        result = await self.db_session.execute(query)

        return result.scalars().all()
