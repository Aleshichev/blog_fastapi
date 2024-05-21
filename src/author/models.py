# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from src.database import Base

# class Author(Base):
#     __tablename__ = "authors"
#     id: int = Column(Integer, primary_key=True)
#     name: str = Column(String(length=50), nullable=False)
#     last_name: str = Column(String(length=50), nullable=False)
    
#     posts = relationship("Post", back_populates="author")
