from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import os
import sys
from eralchemy2 import render_er

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(String(400), nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(500), nullable=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Non column properties
    followers = relationship("Follower", foreign_keys="Follower.user_to_id", backref="followed_user")
    following = relationship("Follower", foreign_keys="Follower.user_from_id", backref="follower_user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    caption: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    location: Mapped[str] = mapped_column(String(200), nullable=True)


class Coment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)  # Follower ID
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)  # Followed one ID
    follow_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)


class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    like_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)


# Draw from SQLAlchemy base
try:
    result = render_er(db.Model, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
