from courses.models import Course
from users.models import User
from utils.repository_base import RepositoryBase


class CourseRepo(RepositoryBase):

    async def create_course(self, title: str, description: str, owner: User) -> Course:
        new_course = Course(
            title=title,
            description=description,
            owner=owner
        )
        self.db_session.add(new_course)
        await self.db_session.flush()
        return new_course
