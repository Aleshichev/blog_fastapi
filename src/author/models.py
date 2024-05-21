from sqlalchemy import Column, Integer, String

from src.database import Base

class Author(Base):
    __tablename__ = "authors"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=10), nullable=True)
    last_name: str = Column(String(length=10), nullable=True)
    # posts = relationship("Post", back_populates="author")

