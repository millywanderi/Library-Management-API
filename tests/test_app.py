import unittest
from flask_app import create_app, db
from config import TestingConfig, ProductionConfig


class TestLibraryApi(unittest.TestCase):

    def setUp(self):
        """Runs before each test"""

        self.app = create_app(ProductionConfig)

        # Override DB for testing
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config['TESTING'] = True

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        """Runs after each test"""

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # ------------------------
    # USER TESTS
    # ------------------------

    def test_create_user(self):
        response = self.client.post('/users', json={
            "name": "Millicent Wanderi",
            "email": "millicentw@example.com"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], "Millicent Wanderi")

    def test_get_users(self):
        self.client.post('/users', json={
            "name": "Millicent Wanderi",
            "email": "millicentw@example.com"
        })

        response = self.client.get('/users')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

    def test_get_single_user(self):
        res = self.client.post('/users', json={
            "name": "Millicent",
            "email": "millicent@example.com"
        })

        user_id = res.get_json()['id']

        response = self.client.get(f'/users/{user_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], "Millicent")

    def test_update_user(self):
        res = self.client.post('/users', json={
            "name": "Bob",
            "email": "bob@example.com"
        })

        user_id = res.get_json()['id']

        response = self.client.put(f'/users/{user_id}', json={
            "name": "Bob Updated",
            "email": "bob2@example.com"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], "Bob Updated")

    def test_delete_user(self):
        res = self.client.post('/users', json={
            "name": "ToDelete",
            "email": "todelete@example.com"
        })

        user_id = res.get_json()['id']

        response = self.client.delete(f'/users/{user_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted", data['message'])

    # --------------------
    # BOOK TESTS
    # --------------------

    def test_create_book(self):
        response = self.client.post('/books', json={
            "title": "Flask Guide",
            "author": "Miguel"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['title'], "Flask Guide")

    # --------------------
    # RELATIONSHIP TESTS
    # --------------------

    def test_allocate_book(self):
        user = self.client.post('/users', json={
            "name": "Reader",
            "email": "reader@example.com"
        }).get_json()

        book = self.client.post('/books', json={
            "title": "Book A",
            "author": "Author A"
        }).get_json()

        response = self.client.get(
            f"/users/{user['id']}/add_book/{book['id']}"
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("allocated", data['message'])

    def test_allocate_multiple_books(self):
        user = self.client.post('/users', json={
            "name": "Multiuser",
            "email": "multiuser@example.com"
        }).get_json()

        book1 = self.client.post('/books', json={
            "title": "Book A",
            "author": "A"
        }).get_json()

        book2 = self.client.post('/books', json={
            "title": "Book B",
            "author": "B"
        }).get_json()

        response = self.client.post(
            f"/users/{user['id']}/add_books",
            json={
                "book_ids": [book1['id'], book2['id']]
            }
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "All books allocated!")


if __name__ == '__main__':
    unittest.main()
