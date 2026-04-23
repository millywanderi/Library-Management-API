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
