from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def list(self):
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, id):
        raise NotImplementedError


class RepositoryBase(AbstractRepository):
    model = None

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self,  data: dict):
        query = insert(self.model).values(**data).returning(self.model)
        res = await self.db_session.execute(query)
        await self.db_session.commit()
        return res.scalar_one_or_none()

    async def list(self):
        query = select(self.model)
        res = await self.db_session.execute(query)

        return res.scalars().all()

    async def retrieve(self, id: str):
        query = select(self.model).where(self.model.id == id)
        result = await self.db_session.execute(query)

        instance = result.scalar_one_or_none()

        return instance
