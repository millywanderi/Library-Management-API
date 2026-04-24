import unittest
from app import app, db, User, Book


class TestLibraryApi(unittest.TestCase):

    def SetUp(self):
        """Runs before each test"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///:memory'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Runs after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # ------------------------
    # USER TESTS
    # ------------------------
    def test_create_user(self):
        payload = {
            "name": "Millicent Wanderi",
            "email": "millicentw@example.com"
        }

        response = self.app.post('/users', json=payload)
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


