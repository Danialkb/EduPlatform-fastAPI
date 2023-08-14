from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import SECRET_KEY, ALGORITHM
from database import get_session
from users.repository import UserRepo
from users.services import UserService, oauth2schema
from utils.unit_of_work import UnitOfWorkBase, UnitOfWork


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


async def get_user_service(uow: UnitOfWorkBase = Depends(UnitOfWork)):
    return UserService(uow)
