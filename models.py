# SQL Alchemy Constructor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from flask_login import UserMixin

from app import db  # Ensure that db is imported from app.py


# defining the models ( some sort object that translate to a SQL table)
# user model
class User(db.Model, UserMixin):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)

    posts = db.relationship("Post", backref="author_obj", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# post model
class Post(db.Model):

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(255), nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # Assuming a User model
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    date_posted: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    def __repr__(self):
        return f"<Post {self.title} by {self.author}>"
