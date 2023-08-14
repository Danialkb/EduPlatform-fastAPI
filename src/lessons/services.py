from utils.unit_of_work import UnitOfWorkBase


class LessonService:
    def __init__(self, uow: UnitOfWorkBase):
        self.uow = uow


