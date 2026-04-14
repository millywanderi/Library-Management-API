# 📚 Library Management API

A RESTful API built with **Flask**, **SQLAlchemy**, and **MySQL** for managing users and books, including assigning books to users.

---

## 🚀 Features

* Create, read, update, and delete users
* Create books
* Assign a single book to a user
* Assign multiple books to a user
* Prevent duplicate book allocations
* Many-to-many relationship between users and books

---

## 🛠️ Tech Stack

* Python 3.12
* Flask
* SQLAlchemy (ORM)
* Marshmallow (Serialization & Validation)
* MySQL

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Library-Management-API
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install flask flask_sqlalchemy flask_marshmallow mysql-connector-python
```

### 4. Configure Database

Update your database connection string in `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/Library_Management_API'
```

Then create the database in MySQL:

```sql
CREATE DATABASE Library_Management_API;
```

### 5. Run the Application

```bash
python app.py
```

The API will be available at:

```
http://127.0.0.1:5000/
```

---

## 📦 API Endpoints

### 👤 Users

#### Create User

```http
POST /users
```

**Body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

#### Get All Users

```http
GET /users
```

---

#### Get Single User

```http
GET /users/<id>
```

---

#### Update User

```http
PUT /users/<id>
```

**Body:**

```json
{
  "name": "Updated Name",
  "email": "updated@example.com"
}
```

---

#### Delete User

```http
DELETE /users/<id>
```

---

### 📚 Books

#### Create Book

```http
POST /books
```

**Body:**

```json
{
  "title": "Clean Code",
  "author": "Robert C. Martin"
}
```

---

### 🔗 Book Allocation

#### Assign Single Book to User

```http
GET /users/<user_id>/add_book/<book_id>
```

---

#### Assign Multiple Books to User

```http
POST /users/<user_id>/add_books
```

**Body:**

```json
{
  "book_ids": [1, 2, 3]
}
```

---

## 🧠 Data Model

### User

* `id` (Primary Key)
* `name`
* `email`

### Book

* `id` (Primary Key)
* `title`
* `author`

### Relationship

* Many-to-Many between Users and Books via `user_book` table

---

## ⚠️ Error Handling

* Returns `400 Bad Request` for invalid input
* Prevents duplicate book assignments
* Skips invalid book IDs when assigning multiple books

---

## 🧪 Example Workflow

1. Create a user
2. Create books
3. Assign books to the user
4. Retrieve user data

---

## 📌 Notes

* Ensure MySQL server is running before starting the app
* The app uses `db.create_all()` to automatically create tables
* Duplicate book allocations are prevented at the application level

---

## 👩‍💻 Author

**Millicent Wanderi**
Backend Software Engineer

---

## 📄 License

This project is open-source and available for learning and development purposes.
