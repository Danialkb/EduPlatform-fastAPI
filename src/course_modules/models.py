import uuid

from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Module(Base):
    __tablename__ = "course_module"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('course.id'))

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module")

    def as_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            course_id=self.course_id,
            lessons=[lesson.as_dict() for lesson in self.lessons]
        )
