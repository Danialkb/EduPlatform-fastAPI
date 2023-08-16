import uuid

from sqlalchemy import Column, String, UUID, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from course_modules.models import CourseModule


class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    video = Column(String, nullable=True)
    module_id = Column(UUID(as_uuid=True), ForeignKey("course_module.id"))

    module = relationship("CourseModule", back_populates="lessons")

    def as_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            content=self.content,
            video=self.video,
            module_id=self.module_id,
        )

