import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from utils.repository_base import RepositoryBase


class UserRepo(RepositoryBase):

    async def create_user(
            self, name: str, surname: str, email: str, password: str
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            password=password
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
