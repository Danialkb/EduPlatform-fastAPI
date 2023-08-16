from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from courses.permissions import is_course_owner
from lessons.dependencies import get_lesson_service
from lessons.schemas import CreateLesson
from lessons.services import LessonService
from users.dependencies import get_current_user
from users.models import User

router = APIRouter(prefix="", tags=["Lessons"])


@router.post("/{course_id}/modules/{module_id}/lessons/")
async def add_lesson(
        course_id: str,
        module_id: str,
        body: CreateLesson,
        user: User = Depends(get_current_user),
        lesson_service: LessonService = Depends(get_lesson_service),
):
    if not is_course_owner(user, course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized access only"
        )

    return await lesson_service.create_lesson(body, module_id)
