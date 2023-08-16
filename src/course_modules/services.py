from course_modules.models import CourseModule
from course_modules.schemas import CourseModuleCreate
from utils.unit_of_work import UnitOfWorkBase


class CourseModuleService:
    def __init__(self, uow: UnitOfWorkBase):
        self.uow = uow

    async def get_course_modules(self, course_id: str):
        async with self.uow:
            res = await self.uow.course_modules.list(course_id)
            modules = []

            for module in res:
                modules.append(module.as_dict())

            return modules

    async def create_module(self, course_module: CourseModuleCreate, course_id: str):
        async with self.uow:
            module = await self.uow.course_modules.create({
                **course_module.dict(),
                "course_id": course_id
            })
            await self.uow.commit()

            return module
