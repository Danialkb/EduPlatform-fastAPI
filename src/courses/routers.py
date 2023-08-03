from fastapi import APIRouter, Depends, Request, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from courses.schemas import ShowCourse, CourseCreate
from courses.services import CourseService
from database import get_session
from users.models import User, RoleEnum
from users.services import get_current_user

router = APIRouter(prefix='/courses', tags=['Courses'])


@router.post('/', response_model=ShowCourse)
async def create_course(
        title: str = Form(...),
        description: str = Form(...),
        logo: UploadFile = File(None),
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user),
) -> ShowCourse:
    course_service = CourseService(session)
    if not user or user.role != RoleEnum.TUTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="authorized access only"
        )
    body = CourseCreate(title=title, description=description)
    result = await course_service.create_course(body, user.id, logo)
    return result


@router.post("/file/")
async def upload_file(logo: UploadFile = File(...)):
    return {"filename": logo.filename}


@router.get("/")
async def get_courses(session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)

    return await course_service.get_courses()

