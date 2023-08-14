
from sqlalchemy import insert, select

from categories.models import Category
from utils.repository_base import RepositoryBase
from categories.models import course_category


class CategoryRepo(RepositoryBase):
    model = Category

    async def add_categories_for_course(self, course_id, category_slug: str):
        query = select(self.model).where(self.model.name == category_slug)

        result = await self.db_session.execute(query)
        category = result.scalar_one()
        if not await self._category_course_relation_exists(category.id, course_id):
            query = insert(course_category).values(
                category_id=category.id,
                course_id=course_id
            )
            await self.db_session.execute(query)

    async def _category_course_relation_exists(self, category_id, course_id):
        query = select(course_category).where(
            course_category.c.category_id == category_id,
            course_category.c.course_id == course_id
        )

        result = await self.db_session.execute(query)
        relation = result.all()

        if len(relation) == 0:
            return False
        return True
