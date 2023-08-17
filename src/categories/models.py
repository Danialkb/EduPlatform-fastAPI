import uuid

from sqlalchemy import Column, UUID, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


course_category = Table(
    "course_category_association",
    Base.metadata,
    Column("category_id", UUID(as_uuid=True), ForeignKey('category.id')),
    Column("course_id", UUID(as_uuid=True), ForeignKey('course.id')),
)


class Category(Base):
    __tablename__ = "category"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    courses = relationship("Course", secondary=course_category, back_populates="categories")

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
        )
