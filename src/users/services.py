from datetime import datetime, timedelta
from typing import Union, Any

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES
from database import get_session
from users.repository import UserRepo
from users.schemas import UserCreate, ShowUser, Token, UserAuth


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepo(session)
        self._password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._auth_service = _AuthenticationService()

    async def create_new_user(self, body: UserCreate) -> ShowUser:
        body.password = self._hash_password(body.password)

        user = await self.repo.create(body.dict())

        return ShowUser(
            user_id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            role=user.role
        )

    async def verify_user(self, creds) -> Token:
        user = await self.repo.get_user_by_email(creds.username)
        if not self._verify_password(creds.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
        return Token(
            access_token=self._auth_service.create_access_token(creds.username),
            type="bearer",
        )

    async def get_user(self, id: str) -> ShowUser:
        user = await self.repo.retrieve(id)

        return ShowUser(
            user_id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            role=user.role
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


async def get_current_user(
        token: str = Depends(oauth2schema), db_session: AsyncSession = Depends(get_session)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate credentials"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credentials"
        )

    repo = UserRepo(db_session)
    user = await repo.get_user_by_email(email)
    return user
