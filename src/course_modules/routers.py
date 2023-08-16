from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from course_modules.dependencies import get_course_module_service
from course_modules.schemas import CourseModuleCreate
from course_modules.services import CourseModuleService
from courses.permissions import is_course_owner
from users.dependencies import get_current_user
from users.models import User

router = APIRouter(prefix="", tags=["Course Modules"])


@router.post("/{course_id}/modules/")
async def create_module(
        course_id: str,
        course_module: CourseModuleCreate,
        user: User = Depends(get_current_user),
        course_module_service: CourseModuleService = Depends(get_course_module_service),
):
    if not is_course_owner(user, course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized access only"
        )

    return await course_module_service.create_module(course_module, course_id)


@router.get("/{course_id}/modules/")
async def get_course_modules(
        course_id: str,
        course_module_service: CourseModuleService = Depends(get_course_module_service),
):
    return await course_module_service.get_course_modules(course_id)


@router.get("/modules/{module_id}/")
async def get_module(
        module_id: str,
        course_module_service: CourseModuleService = Depends(get_course_module_service),
):
    return await course_module_service.get_module(module_id)


@router.delete("/{course_id}/modules/{module_id}/")
async def delete_module(
        course_id: str,
        module_id: str,
        user: User = Depends(get_current_user),
        course_module_service: CourseModuleService = Depends(get_course_module_service),
):
    if not is_course_owner(user, course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized access only"
        )
    return await course_module_service.delete_module(module_id)
