from datetime import datetime
from typing import Optional

from fastapi import HTTPException, UploadFile
from starlette import status

from courses.schemas import CourseCreate, ShowCourse, AddDeleteStudent
from utils.unit_of_work import UnitOfWorkBase


class FilesService:

    async def save_logo(self, file: UploadFile) -> str:
        if not await self._is_image(file):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Only image files are allowed for the logo."
            )

        filename = datetime.today().strftime("%Y-%m-%d") + file.filename
        content = await file.read()
        with open(f'/Users/mak/PycharmProjects/EducationPlatform/src/media/course_logos/{filename}', 'wb') as f:
            f.write(content)
        return filename

    @staticmethod
    async def _is_image(file: UploadFile) -> bool:
        return file and file.content_type.startswith("image/")


class CourseService:
    def __init__(self, uow: UnitOfWorkBase):
        self.uow = uow
        self.files_service = FilesService()

    async def create_course(self, body: CourseCreate, owner_id: str, file: Optional[UploadFile]):
        async with self.uow:
            filename = None
            if file:
                filename = await self.files_service.save_logo(file)
                filename = 'course_logos/' + filename

            data = {**body.dict(), "owner_id": owner_id}
            if filename:
                data['logo'] = filename

            course = await self.uow.courses.create(data)
            loaded_course = await self.uow.courses.retrieve_with_related(course.id, "owner")

            return ShowCourse(
                title=course.title,
                description=course.description,
                owner=f'{loaded_course.owner.name} {loaded_course.owner.surname}'
            )

    async def get_courses(self):
        async with self.uow:
            courses = await self.uow.courses.list()
            course_list: list[ShowCourse] = []

            for course in courses:
                course_list.append(
                    ShowCourse(
                        title=course.title,
                        description=course.description,
                        owner=str(course.owner_id),
                    )
                )

            return course_list

    async def get_course(self, id: str):
        async with self.uow:
            course = await self.uow.courses.retrieve_with_related(id, "owner")

            return ShowCourse(
                title=course.title,
                description=course.description,
                owner=f"{course.owner.name} {course.owner.surname}"
            )

    async def get_course_students(self, id: str):
        async with self.uow:
            return await self.uow.courses.get_course_students(id)

    async def add_student(self, id: str, body: AddDeleteStudent):
        async with self.uow:
            return await self.uow.courses.add_student(id, body.email)

    async def delete_student(self, id: str, body:  AddDeleteStudent):
        async with self.uow:
            return await self.uow.courses.delete_student(id, body.email)
