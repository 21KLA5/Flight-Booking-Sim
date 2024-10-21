import unittest
from app import app, database  # Import the app and mock database

class LogInTestCase(unittest.TestCase):

    # Set up the Flask test client
    def setUp(self):
        self.app = app.test_client()  # Flask's test client
        self.app.testing = True
    
    # Test login with valid credentials
    def test_login_success(self):
        # First, register a user
        database['terencejiang@gmail.com'] = {
            'firstName': 'Terence',
            'lastName': 'Jiang',
            'password': 'password123'
        }

        response = self.app.post('/login', data={
            'email': 'terencejiang@gmail.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertIn('/profile', response.headers['Location'])  # Check redirection to index page

    # Test login with incorrect password
    def test_login_incorrect_password(self):
        # Register a user with known password
        database['jackcam@gmail.com'] = {
            'firstName': 'Jack',
            'lastName': 'Cam',
            'password': 'password123'
        }

        response = self.app.post('/login', data={
            'email': 'jackcam@gmail.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the login page
        self.assertIn(b'Email and password does not match', response.data)  # Check if the error message is shown

    # Test login with unregistered email
    def test_login_unregistered_email(self):
        response = self.app.post('/login', data={
            'email': 'nonexistent@gmail.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the login page
        self.assertIn(b'The provided email is not registered', response.data)  # Check if the error message is shown


if __name__ == '__main__':
    unittest.main()
