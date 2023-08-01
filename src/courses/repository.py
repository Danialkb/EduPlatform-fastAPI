from courses.models import Course
from courses.schemas import CourseCreate
from users.models import User
from utils.repository_base import RepositoryBase


class CourseRepo(RepositoryBase):

    async def create_course(self, body: CourseCreate) -> Course:
        new_course = Course(**body.dict())
        self.db_session.add(new_course)
        await self.db_session.flush()
        return new_course
