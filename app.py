#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import ForeignKey, Table, Column, String, Integer
from marshmallow import ValidationError
from typing import List, Optional

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://millie:ciku2015@localhost/Library_Management_API'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating our Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

# Association Table
user_book = Table(
    "user_book"
    BaseMeta,
    Column("user_id", ForeignKey("user_account.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True)
)

# Models
# User Model
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200))

    #One-to-Many relationship from this User to a List of Book Objects
    books: Mapped[List["Book"]] = relationship(
            "Pet",
            secondary=user_book,
            back_populates="users"
    )


# Book Model
class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(100))

    #One-to-Many relationship,1 book can be related to a List of Users
    users: Mapped[List["User"]] = relationship(
            "User",
            secondary=user_book,
            back_populates="books"
    )

