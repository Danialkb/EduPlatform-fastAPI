from sqlalchemy.ext.asyncio import AsyncSession

from courses.repository import CourseRepo
from courses.schemas import CourseCreate, ShowCourse


class CourseService:
    def __init__(self, session: AsyncSession):
        self.repo = CourseRepo(session)

    async def create_course(self, body: CourseCreate):
        async with self.repo.db_session.begin():
            course = await self.repo.create_course(
                title=body.title,
                description=body.description,
                owner=body.owner
            )

            return ShowCourse(
                title=course.title,
                description=course.description,
                owner=f'{course.owner.name} {course.owner.surname}'
            )
