from typing import List

from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload, joinedload
from starlette import status

from course_modules.models import Module
from courses.models import Course, association_table
from users.repository import UserRepo
from utils.repository_base import RepositoryBase


class CourseRepo(RepositoryBase):
    model = Course

    async def get_course_students(self, id):
        query = select(Course)\
            .where(Course.id == id)\
            .options(selectinload(Course.students))
        result = await self.db_session.execute(query)

        return result.scalars().all()

    async def get_full_course(self, id: str):
        query = select(Course).where(Course.id == id).options(
            joinedload(Course.owner),
            joinedload(Course.modules).options(selectinload(Module.lessons)),
            # joinedload(Course.modules).options(selectinload(Module.lessons))
        )

        res = await self.db_session.execute(query)
        return res.scalars().unique().first()

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

        return {"status": "success"}

    async def delete_student(self, id: str, student_email: str):
        user_service = UserRepo(self.db_session)
        student = await user_service.get_user_by_email(student_email)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No such student"
            )
        query = delete(association_table) \
            .where(association_table.c.student_id == student.id) \
            .where(association_table.c.course_id == id)
        await self.db_session.execute(query)

        return {"status":  "deleted"}
