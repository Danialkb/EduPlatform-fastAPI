from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr


class CourseCreate(BaseModel):
    title: str
    description: str


class ShowCourse(BaseModel):
    title: str
    description: str
    owner: str


class AddDeleteStudent(BaseModel):
    email: EmailStr
