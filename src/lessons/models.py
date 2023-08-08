import uuid

from sqlalchemy import Column, String, UUID, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    video = Column(String, nullable=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey('course.id'))

    course = relationship("Course", back_populates="lessons")

