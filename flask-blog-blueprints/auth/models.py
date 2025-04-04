from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin

from db import db  # Ensure that db is imported from app.py


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