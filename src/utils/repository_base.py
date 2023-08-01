from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryBase(ABC):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
