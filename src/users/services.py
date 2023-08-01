import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from users.repository import UserRepo
from users.schemas import UserCreate, ShowUser
from utils.service_base import ServiceBase


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepo(session)

    async def create_new_user(self, body: UserCreate) -> ShowUser:
        async with self.repo.db_session.begin():
            try:
                hashed_password = bcrypt.hashpw(body.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            except UnicodeEncodeError:
                raise Exception('Your password contains restricted symbols')
            user = await self.repo.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
                password=hashed_password
            )
            return ShowUser(
                user_id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
            )
