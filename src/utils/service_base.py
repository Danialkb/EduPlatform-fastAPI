from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from utils.repository_base import RepositoryBase


class ServiceBase(ABC):
    def __init__(self, session: AsyncSession):
        self.repo = RepositoryBase(session)
