from pydantic import BaseModel


class CreateLesson(BaseModel):
    title: str
