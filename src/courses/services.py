from datetime import datetime
from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from courses.repository import CourseRepo
from courses.schemas import CourseCreate, ShowCourse, AddDeleteStudent


class CourseFilesService:

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
    def __init__(self, session: AsyncSession):
        self.repo = CourseRepo(session)
        self.files_service = CourseFilesService()

    async def create_course(self, body: CourseCreate, owner_id: str, file: Optional[UploadFile]):
        filename = None
        if file:
            filename = await self.files_service.save_logo(file)
            filename = 'media/course_logos/' + filename

        course = await self.repo.create(data={**body, "owner_id": owner_id, "filename": filename})

        return ShowCourse(
            title=course.title,
            description=course.description,
            owner=f'{course.owner.name} {course.owner.surname}'
        )

    async def get_courses(self):
        courses = await self.repo.list()
        return courses

    async def get_course(self, id: str):
        course = await self.repo.retrieve_with_related(id, "owner")

        return ShowCourse(
            title=course.title,
            description=course.description,
            owner=f"{course.owner.name} {course.owner.surname}"
        )

    async def get_course_students(self, id: str):
        return await self.repo.get_course_students(id)

    async def add_student(self, id: str, body: AddDeleteStudent):
        return await self.repo.add_student(id, body.email)

    async def delete_student(self, id: str, body:  AddDeleteStudent):
        return await self.repo.delete_student(id, body.email)
