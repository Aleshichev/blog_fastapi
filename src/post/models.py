# from datetime import datetime
# from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
# from sqlalchemy.orm import relationship
# from src.database import Base

# class Post(Base):
#     __tablename__ = "posts"
#     id: int = Column(Integer, primary_key=True, index=True)
#     title: str = Column(String(length=100), index=True, nullable=False)
#     content: str = Column(Text(length=2000), nullable=False)
#     author_id: int = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))
#     category_id: int = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
#     created_at: datetime = Column(DateTime, default=func.now())

#     author = relationship("Author", back_populates="posts")
#     category = relationship("Category", back_populates="posts")
#     tags = relationship("Tag", secondary="post_tags", back_populates="posts")

# class PostTag(Base):
#     __tablename__ = "post_tags"
#     post_id: int = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
#     tag_id: int = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)