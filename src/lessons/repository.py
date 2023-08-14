from lessons.models import Lesson
from utils.repository_base import RepositoryBase


class LessonRepo(RepositoryBase):
    model = Lesson
