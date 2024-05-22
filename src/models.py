from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Table, func
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class Author(Base):
    __tablename__ = "authors"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(length=50), nullable=False)
    email: str = Column(String(length=100), nullable=False, unique=True) 
    photo = Column(String(500))
    posts = relationship("Post", back_populates="author")

class Category(Base):
    __tablename__ = "categories"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(length=100), index=True, nullable=False, unique=True)
    description: str = Column(String(length=255), nullable=True)
    posts = relationship("Post", back_populates="category", cascade="all, delete-orphan")

class Tag(Base):
    __tablename__ = "tags"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(length=50), nullable=False, unique=True)
    posts = relationship("Post", secondary="post_tags", back_populates="tags")

class Post(Base):
    __tablename__ = "posts"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(length=100), index=True, nullable=False, unique=True)
    content: str = Column(Text, nullable=False)
    author_id: int = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))
    category_id: int = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    created_at: datetime = Column(DateTime, default=func.now())
    
    author = relationship("Author", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    tags = relationship("Tag", secondary="post_tags", back_populates="posts")
