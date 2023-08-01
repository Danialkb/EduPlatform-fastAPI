from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from courses.schemas import ShowCourse, CourseCreate
from courses.services import CourseService
from database import get_session

router = APIRouter(prefix='/courses', tags=['Courses'])


@router.post('/', response_model=ShowCourse)
async def create_course(body: CourseCreate, session: AsyncSession = Depends(get_session)) -> ShowCourse:
    course_service = CourseService(session)
    return await course_service.create_course(body)
