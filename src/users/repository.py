from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from users.models import User
from users.schemas import UserCreate
from utils.repository_base import RepositoryBase


class UserRepo(RepositoryBase):

    async def create_user(
            self, body: UserCreate
    ) -> User:
        new_user = User(**body.dict())

        self.db_session.add(new_user)
        await self.db_session.commit()

        return new_user

    async def get_user_by_email(self, email: str):
        query = (
            select(User)
            .where(User.email == email)
            .options(selectinload(User.courses))
        )
        result = await self.db_session.execute(query)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )

        return result.scalar_one_or_none()

    async def get_user(self, id: str):
        query = select(User).where(User.id == id)
        result = await self.db_session.execute(query)

        return result.scalar_one_or_none()
