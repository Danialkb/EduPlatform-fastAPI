from pydantic import BaseModel


class CourseModuleCreate(BaseModel):
    title: str
