from pydantic import BaseModel

from users.schemas import ShowUser


class CourseCreate(BaseModel):
    title: str
    description: str
    owner: ShowUser


class ShowCourse(BaseModel):
    title: str
    description: str
    owner: str
