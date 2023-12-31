import uuid
import enum

from sqlalchemy import Column, UUID, String, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship

from courses.models import association_table
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    password = Column(String(length=1024), nullable=False)

    courses = relationship("Course", back_populates="owner")
    enrolled_courses = relationship("Course", secondary=association_table, back_populates="students")

    def as_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
        }
