from lessons.schemas import CreateLesson
from utils.unit_of_work import UnitOfWorkBase


class LessonService:
    def __init__(self, uow: UnitOfWorkBase):
        self.uow = uow

    async def create_lesson(self, lesson_body: CreateLesson, module_id: str):
        async with self.uow:
            lesson = await self.uow.lessons.create(data={**lesson_body.dict(), "module_id": module_id})

            await self.uow.commit()
            return lesson

    async def get_lessons(self):
        async with self.uow:
            lessons = await self.uow.lessons.list()
            return [lesson.as_dict() for lesson in lessons]
