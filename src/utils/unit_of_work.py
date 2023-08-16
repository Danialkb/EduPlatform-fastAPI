from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from categories.repository import CategoryRepo
from course_modules.repos import CourseModuleRepo
from courses.repository import CourseRepo
from users.repository import UserRepo


class UnitOfWorkBase(ABC):
    users: UserRepo
    courses: CourseRepo
    categories: CategoryRepo
    course_modules: CourseModuleRepo

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.users = UserRepo(self.session)
        self.courses = CourseRepo(self.session)
        self.categories = CategoryRepo(self.session)
        self.course_modules = CourseModuleRepo(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
