#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column, String, Integer, select
from marshmallow import ValidationError
from typing import List, Optional

# Initialize Flask app
app = Flask(__name__)

# Creating our Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy (DO NOT bind yet)
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

# Function to configure app
def configure_app(database_uri=None):
    if database_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://millie:ciku2015@localhost/Library_Management_API'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # NOW initialize extensions
    db.init_app(app)
    ma.init_app(app)

# Association Table
user_book = Table(
    "user_book",
    Base.metadata,
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
            "Book",
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

# Marshmallow Schemas
# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


# Book Schema
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Create endpoints
# Create User
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_user = User(name=user_data['name'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

# Read All Users
@app.route('/users', methods=['Get'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()

    return users_schema.jsonify(users), 200

# Read a Single User by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

# Update User
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid User id"}), 400

    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user.name = user_data['name']
    user.email = user_data['email']

    db.session.commit()
    return user_schema.jsonify(user), 200

# Delete User
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"successfully deleted user {id}"}), 200

# Create Book and Associate Books with Users
# Create a Book
@app.route('/books', methods=['POST'])
def create_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.message), 400

    new_book = Book(title=book_data['title'], author=book_data['author'])
    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book), 201

# Associate a Single Book with a User
@app.route('/users/<int:user_id>/add_book/<int:book_id>', methods=['Get'])
def allocate_book(user_id, book_id):
    user = db.session.get(User, user_id)
    book = db.session.get(Book, book_id)

    user.books.append(book)
    db.session.commit()
    return jsonify({"message": f"{user.name} allocated the {book.author}, {book.title}!"}), 200

# Associate Multiple Books with a User
@app.route('/users/<int:user_id>/add_books', methods=['POST'])
def allocate_books(user_id):
    user = db.session.get(User, user_id)
    book_data = request.json
    
    if not book_data or 'book_ids' not in book_data:
        return jsonify({"error": "book_ids is not required!"}), 400


    for book_id in book_data['book_ids']:
        book = db.session.get(Book, book_id)

        if not book:
            continue

        if book not in user.books:
            user.books.append(book)
        
    db.session.commit()

    return jsonify({"message": "All books allocated!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
