from typing import List

from fastapi import HTTPException
from sqlalchemy import select, insert
from starlette import status

from courses.models import Course, association_table
from courses.schemas import CourseCreate
from users.repository import UserRepo
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

    async def get_course(self, id: str) -> Course:
        query = select(Course).where(Course.id == id)
        result = await self.db_session.execute(query)

        return result.scalar_one_or_none()

    async def add_student(self, id: str, student_email: str):
        user_service = UserRepo(self.db_session)
        student = await user_service.get_user_by_email(student_email)
        query = select(association_table)\
            .where(association_table.c.student_id == student.id)\
            .where(association_table.c.course_id == id)

        result = await self.db_session.execute(query)
        enrolled_student = result.scalar_one_or_none()

        if enrolled_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already enrolled this course"
            )

        query = insert(association_table).values(
            course_id=id,
            student_id=student.id
        )

        await self.db_session.execute(query)
        await self.db_session.commit()

        return {"status": "success"}
