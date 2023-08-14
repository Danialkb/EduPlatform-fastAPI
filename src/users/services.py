from datetime import datetime, timedelta
from typing import Union, Any

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from starlette import status

from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES

from users.schemas import UserCreate, ShowUser, Token
from utils.unit_of_work import UnitOfWorkBase


class UserService:
    def __init__(self, uow: UnitOfWorkBase):
        self.uow = uow
        self._password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._auth_service = _AuthenticationService()

    async def create_new_user(self, body: UserCreate) -> ShowUser:
        async with self.uow:
            body.password = self._hash_password(body.password)

            user = await self.uow.users.create(body.dict())

            await self.uow.commit()

            return ShowUser(
                user_id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
            )

    async def verify_user(self, creds) -> Token:
        async with self.uow:
            user = await self.uow.users.get_user_by_email(creds.username)
            if not user or not self._verify_password(creds.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect email or password"
                )
            return Token(
                access_token=self._auth_service.create_access_token(creds.username),
                type="bearer",
            )

    async def get_user(self, id: str) -> ShowUser:
        async with self.uow:
            user = await self.uow.users.retrieve(id)

            return ShowUser(
                user_id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
            )

    def _hash_password(self, password: str) -> str:
        return self._password_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._password_context.verify(plain_password, hashed_password)


class _AuthenticationService:

    @staticmethod
    def create_access_token(subject: Union[str, Any]) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

        return encoded_jwt

    # @staticmethod
    # def create_refresh_token(subject: Union[str, Any]) -> str:
    #     expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    #
    #     to_encode = {"exp": expires_delta, "sub": str(subject)}
    #     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    #
    #     return encoded_jwt


oauth2schema = OAuth2PasswordBearer(tokenUrl="/users/token/")
