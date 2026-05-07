import unittest
from app import app, db, configure_app


class TestLibraryApi(unittest.TestCase):

    def setUp(self):
        """Runs before each test"""
        configure_app('sqlite:///:memory:')

        app.config['TESTING'] = True
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///:memory'
        
        self.app_context = app.app_context()
        self.app_context.push()
        
        db.create_all()

        self.app = app.test_client()

    def tearDown(self):
        """Runs after each test"""    
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # ------------------------
    # USER TESTS
    # ------------------------
    def test_create_user(self):
        response = self.app.post('/users', json={
            "name": "Millicent Wanderi",
            "email": "millicentw@example.com"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], "Millicent Wanderi")

    def test_get_users(self):
        self.app.post('/users', json={
            "name": "Millicent Wanderi",
            "email": "millicentw@example.com"
        })

        response = self.app.get('/users')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.asserEqual(len(data), 1)

    def test_get_single_user(self):
        res = self.app.post('/users', json={
            "name": "Millicent",
            "email": "millicent@example"
        })

        user_id = res.get_json()['id']

        response = self.app.get(f'/users/{user_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], "Millicent")

    def test_update_user(self):
        res = self.app.post('/users', json={
            "name": "Bob",
            "email": "bob@example.com"
        })

        user_id = res.et_json()['id']

        response = self.app.put(f'/users/{user_id}', json={
            "name": "Bob Updated",
            "email": "bob2@example.com"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], "Bob Updated")

    def test_delete_user(self):
        res = self.app.post('/users', json={
            "name": "ToDelete",
            "email": "todelete@example.com"
        })

        user_id = res.get_json()['id']

        response = self.app.delete(f'/user/{user_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted", data['message'])

    # --------------------
    # Book tests
    # --------------------

    def test_create_book(self):
        response = self.app.post('/books', json={
            "title": "Flask Guide",
            "author": "Minguel"
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['title'], "Flask Guide")

        # --------------------
        # Relationship Tests
        # --------------------

        def test_allocate_book(self):
            user = self.app.post('/users', json={
                "name": "Reader",
                "email":"reader@example.com"
            }).get_json()
            
            book = self.app.post('/books', json={
                "title": "Book A",
                "author": "Author A"
            }).get_json()

            response = self.app.get(
                f"/users/{user['id']}/add_book/{book['id']}"
            )

            data = response.get_json()

            self.assertEqual(response.status_code, 201)
            self.assertIn("allocated", data['message'])

        def test_allocate_multiple_books(self):
            user = self.app.post('/users', json={
                "name": "Multiuser",
                "email": "multiuser@example.com"
            }).get_json()

            book1 = self.app.post('/books', json={
                "title": "Book A",
                "author": "A"
            }).get_json()

            book2 = self.app.post('/books', json={
                "title": "Book B",
                "author": "B"
            }).get_json()

            response = self.app.post(f"/users/{user['id']}/add_books", json={
                "book_ids": [book1['id'], book2['id']]
            })

            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], "All books allocated!")


if __name__ == '__main__':
    unittest.main()
