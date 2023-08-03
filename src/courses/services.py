from datetime import datetime
from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from courses.repository import CourseRepo
from courses.schemas import CourseCreate, ShowCourse


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

        course = await self.repo.create_course(body, owner_id, filename)

        return ShowCourse(
            title=course.title,
            description=course.description,
            owner=f'{course.owner.name} {course.owner.surname}'
        )

    async def get_courses(self):
        courses = await self.repo.get_courses()

        if len(courses) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No courses"
            )

        return courses

