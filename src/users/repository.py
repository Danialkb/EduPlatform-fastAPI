from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from users.models import User
from utils.repository_base import RepositoryBase


class UserRepo(RepositoryBase):
    model = User

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
