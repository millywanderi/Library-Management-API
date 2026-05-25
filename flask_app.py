#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column, String, select
from marshmallow import ValidationError
from typing import List
from config import ProductionConfig


# Creating Base Model
class Base(DeclarativeBase):
    pass


# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()


# Association Table
user_book = Table(
    "user_book",
    Base.metadata,
    Column("user_id", ForeignKey("user_account.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True)
)


# User Model
class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200))

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

    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_book,
        back_populates="books"
    )


# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


# Book Schema
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True


# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)


# Create Flask App
def create_app(config_object=None):

    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
        #app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            os.environ.get('SQLALCHEMY_DATABASE_URI')
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # ONLY check for DB in production runtime (not import)
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("Missing DATABASE URL (set in Render env vars)")

    # -----------------------------------
    # USER ROUTES
    # -----------------------------------

    @app.route('/users', methods=['POST'])
    def create_user():
        try:
            user_data = request.json

            new_user = User(
                name=user_data['name'],
                email=user_data['email']
            )

            db.session.add(new_user)
            db.session.commit()

            return user_schema.jsonify(new_user), 201

        except ValidationError as e:
            return jsonify(e.messages), 400

    @app.route('/users', methods=['GET'])
    def get_users():
        query = select(User)
        users = db.session.execute(query).scalars().all()

        return users_schema.jsonify(users), 200

    @app.route('/users/<int:id>', methods=['GET'])
    def get_user(id):
        user = db.session.get(User, id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        return user_schema.jsonify(user), 200

    @app.route('/users/<int:id>', methods=['PUT'])
    def update_user(id):

        user = db.session.get(User, id)

        if not user:
            return jsonify({"message": "Invalid User id"}), 400

        try:
            user_data = request.json

            user.name = user_data['name']
            user.email = user_data['email']

            db.session.commit()

            return user_schema.jsonify(user), 200

        except ValidationError as e:
            return jsonify(e.messages), 400

    @app.route('/users/<int:id>', methods=['DELETE'])
    def delete_user(id):

        user = db.session.get(User, id)

        if not user:
            return jsonify({"message": "Invalid user id"}), 400

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            "message": f"successfully deleted user {id}"
        }), 200

    # -----------------------------------
    # BOOK ROUTES
    # -----------------------------------

    @app.route('/books', methods=['POST'])
    def create_book():

        try:
            book_data = request.json

            new_book = Book(
                title=book_data['title'],
                author=book_data['author']
            )

            db.session.add(new_book)
            db.session.commit()

            return book_schema.jsonify(new_book), 201

        except ValidationError as e:
            return jsonify(e.messages), 400

    # -----------------------------------
    # RELATIONSHIP ROUTES
    # -----------------------------------

    @app.route('/users/<int:user_id>/add_book/<int:book_id>', methods=['GET'])
    def allocate_book(user_id, book_id):

        user = db.session.get(User, user_id)
        book = db.session.get(Book, book_id)

        if not user or not book:
            return jsonify({
                "message": "User or Book not found"
            }), 404

        user.books.append(book)

        db.session.commit()

        return jsonify({
            "message": f"{user.name} allocated {book.title}"
        }), 201

    @app.route('/users/<int:user_id>/add_books', methods=['POST'])
    def allocate_books(user_id):

        user = db.session.get(User, user_id)

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        book_data = request.json

        if not book_data or 'book_ids' not in book_data:
            return jsonify({
                "error": "book_ids is required!"
            }), 400

        for book_id in book_data['book_ids']:

            book = db.session.get(Book, book_id)

            if not book:
                continue

            if book not in user.books:
                user.books.append(book)

        db.session.commit()

        return jsonify({
            "message": "All books allocated!"
        }), 200

    return app



# Run Application
if __name__ == "__main__":

    app = create_app(ProductionConfig)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
