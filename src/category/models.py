# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from src.database import Base

# class Category(Base):
#     __tablename__ = "categories"
#     id: int = Column(Integer, primary_key=True, index=True)
#     name: int = Column(String(length=100), index=True, nullable=False)
#     posts = relationship("Post", back_populates="category")
#     # posts = relationship("Post", back_populates="category", cascade="all, delete-orphan")

