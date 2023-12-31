from users.models import User


def is_course_owner(user: User, course_id: str):
    course_ids = [str(course.id) for course in user.courses]

    if not user or course_id not in course_ids:
        return False

    return True
