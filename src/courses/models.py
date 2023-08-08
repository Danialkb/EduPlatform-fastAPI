import uuid

from sqlalchemy import Column, UUID, ForeignKey, String, Boolean, Table
from sqlalchemy.orm import relationship

from database import Base
from lessons.models import Lesson


association_table = Table(
    'course_student_association',
    Base.metadata,
    Column('course_id', UUID(as_uuid=True), ForeignKey('course.id')),
    Column('student_id', UUID(as_uuid=True), ForeignKey('user.id'))
)


class Course(Base):
    __tablename__ = "course"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    description = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_private = Column(Boolean(), default=True)
    logo = Column(String, default='/course_logos/no-img.png')

    owner = relationship("User", back_populates="courses")
    students = relationship("User", secondary=association_table, back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
