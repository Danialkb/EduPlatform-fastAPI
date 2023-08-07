from courses.models import Course
from users.models import User, RoleEnum


def is_tutor_and_course_owner(user: User, course: Course):
    if not user or user.role != RoleEnum.TUTOR or course not in user.courses:
        return False
    return True
