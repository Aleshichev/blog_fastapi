# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from src.database import Base


# class Tag(Base):
#     __tablename__ = "tags"
#     id: int = Column(Integer, primary_key=True, index=True)
#     name: str = Column(String(length=50), index=True, nullable=False)
#     posts = relationship("Post", secondary="post_tags", back_populates="tags")
