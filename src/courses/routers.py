import asyncio

from fastapi import APIRouter, Depends, Request, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from courses.permissions import is_tutor_and_course_owner
from courses.schemas import ShowCourse, CourseCreate, AddDeleteStudent
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


@router.post("/{id}/add-student/")
async def add_student(
        id: str,
        body: AddDeleteStudent,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
):
    course_service = CourseService(session)
    if not is_tutor_and_course_owner(user, id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="authorized access only"
        )

    result = await course_service.add_student(id, body)

    return result


@router.delete("/{course_id}/delete-student/")
async def delete_student(
        id: str,
        body: AddDeleteStudent,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
):
    course_service = CourseService(session)
    if not is_tutor_and_course_owner(user, id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="authorized access only"
        )

    result = await course_service.delete_student(id, body)

    return result


@router.get("/{course_id}/students/")
async def get_course_students(
        course_id: str,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    course_service = CourseService(session)
    if not is_tutor_and_course_owner(user, course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="authorized access only"
        )

    result = await course_service.get_course_students(course_id)

    return result

@router.get("/")
async def get_courses(session: AsyncSession = Depends(get_session)):
    course_service = CourseService(session)

    return await course_service.get_courses()


@router.get("/{id}/", response_model=ShowCourse)
async def get_course(id: str, session: AsyncSession = Depends(get_session)) -> ShowCourse:
    course_service = CourseService(session)
    return await course_service.get_course(id)
