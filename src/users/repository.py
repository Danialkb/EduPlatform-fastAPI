import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemas import UserCreate
from utils.repository_base import RepositoryBase


class UserRepo(RepositoryBase):

    async def create_user(
            self, body: UserCreate
    ) -> User:
        new_user = User(**body.dict())

        self.db_session.add(new_user)
        await self.db_session.flush()

        return new_user

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)

        return result.scalar_one_or_none()
