from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from starlette import status

from course_modules.dependencies import get_course_module_service
from course_modules.services import CourseModuleService
from courses.permissions import is_course_owner
from courses.schemas import ShowCourse, CourseCreate, AddDeleteStudent
from courses.services import CourseService
from users.dependencies import get_current_user
from users.models import User
from courses.dependencies import get_course_service

router = APIRouter(prefix='/courses', tags=['Courses'])


@router.post('/')
async def create_course(
        title: str = Form(...),
        user: User = Depends(get_current_user),
        course_service: CourseService = Depends(get_course_service)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized access only"
        )
    body = CourseCreate(title=title)
    result = await course_service.create_course(body, user.id)
    return result


@router.put("/course_id/")
async def edit_course(
        id: str,
        description: str = Form(...),
        logo: UploadFile = File(None),
        categories: List[str] = Form(...),
        user: User = Depends(get_current_user),
        course_service: CourseService = Depends(get_course_service),
):
    if not is_course_owner(user, id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized access only"
        )

    return await course_service.edit_course(id, description, logo, categories)


@router.post("/{id}/add-student/")
async def add_student(
        id: str,
        body: AddDeleteStudent,
        user: User = Depends(get_current_user),
        course_service: CourseService = Depends(get_course_service),
):
    if not is_course_owner(user, id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized access only"
        )

    result = await course_service.add_student(id, body)

    return result


@router.delete("/{course_id}/delete-student/")
async def delete_student(
        id: str,
        body: AddDeleteStudent,
        user: User = Depends(get_current_user),
        course_service: CourseService = Depends(get_course_service)
):
    if not is_course_owner(user, id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized access only"
        )

    result = await course_service.delete_student(id, body)

    return result


@router.get("/{course_id}/students/")
async def get_course_students(
        course_id: str,
        user: User = Depends(get_current_user),
        course_service: CourseService = Depends(get_course_service)
):
    if not is_course_owner(user, course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized access only"
        )

    result = await course_service.get_course_students(course_id)

    return result


@router.get("/")
async def get_courses(
        course_service: CourseService = Depends(get_course_service)
):
    return await course_service.get_courses()


@router.get("/{id}/")
async def get_course(
        id: str,
        course_service: CourseService = Depends(get_course_service),
):
    return await course_service.get_course(id)
