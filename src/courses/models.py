import uuid

from sqlalchemy import Column, UUID, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Course(Base):
    __tablename__ = "course"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, unique=True, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    description = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    owner = relationship("User", back_populates="courses")
