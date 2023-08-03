from datetime import datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from courses.repository import CourseRepo
from courses.schemas import CourseCreate, ShowCourse


class CourseFilesService:

    async def save_logo(self, file: UploadFile) -> str:
        print("saving logo")
        filename = datetime.today().strftime("%Y-%m-%d") + file.filename
        content = await file.read()
        with open(f'/Users/mak/PycharmProjects/EducationPlatform/src/media/course_logos/{filename}', 'wb') as f:
            f.write(content)
        return filename


class CourseService:
    def __init__(self, session: AsyncSession):
        self.repo = CourseRepo(session)
        self.files_service = CourseFilesService()

    async def create_course(self, body: CourseCreate, owner_id: str, file: UploadFile):
        filename = await self.files_service.save_logo(file)
        filename = 'media/course_logos/' + filename
        print(filename)
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

