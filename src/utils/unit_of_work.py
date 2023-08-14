from abc import ABC, abstractmethod
from typing import Type

from courses.repository import CourseRepo
from database import async_session
from users.repository import UserRepo


class UnitOfWorkBase(ABC):
    users: UserRepo
    courses: CourseRepo

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepo(self.session)
        self.courses = CourseRepo(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
