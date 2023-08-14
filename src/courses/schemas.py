from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr

from users.schemas import ShowUser


class CourseCreate(BaseModel):
    title: str


class ShowCourse(BaseModel):
    title: str
    description: str | None
    owner: dict


class AddDeleteStudent(BaseModel):
    email: EmailStr
