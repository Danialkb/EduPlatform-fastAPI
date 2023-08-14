from courses.models import Course
from users.models import User, RoleEnum


def is_tutor_and_course_owner(user: User, course_id: str):
    course_ids = [str(course.id) for course in user.courses]

    if not user or user.role != RoleEnum.TUTOR or course_id not in course_ids:
        return False

    return True
