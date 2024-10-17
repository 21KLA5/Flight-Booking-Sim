import unittest
from flask import Flask
from app import app, database  # Import the app and the mock database from your main file

class RegisterTestCase(unittest.TestCase):
    
    # Setup a Flask test client before each test
    def setUp(self):
        self.app = app.test_client()  
        self.app.testing = True       

    # Test case where all fields are filled correctly (successful registration)
    def test_successful_registration(self):
        response = self.app.post('/', data={
            'firstName': 'Kavin',
            'lastName': 'Arasu',
            'email': 'johndoe@gmail.com',
            'password': 'password12',
            'confirmPass': 'password12'
        })
        self.assertEqual(response.status_code, 302)  # 302 checks for redirection to the login page
        self.assertIn('johndoe@gmail.com', database)  # Ensure the user was added to the mock database

    # Test case for when passwords do not match
    def test_password_mismatch(self):
        response = self.app.post('/', data={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'confirmPass': 'password456'
        })
        self.assertEqual(response.status_code, 200)  # Expect 200 OK, meaning it stays on the same page
        self.assertIn(b"Passwords do not match", response.data)  # Check if the error message is in the response

    # Test case for missing fields (empty email)
    def test_missing_field(self):
        response = self.app.post('/', data={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': '',
            'password': 'password123',
            'confirmPass': 'password123'
        })
        self.assertEqual(response.status_code, 200)  # Expect 200 OK, meaning it stays on the same page
        self.assertIn(b"Fill out all fields", response.data)  # Check if the error message is in the response

    # Test case where the email is already registered
    def test_email_already_registered(self):
        # First, add a user to the mock database
        database['johndoe@example.com'] = {'firstName': 'John', 'lastName': 'Doe', 'password': 'password123'}

        response = self.app.post('/', data={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'confirmPass': 'password123'
        })
        self.assertEqual(response.status_code, 200)  # Expect 200 OK, meaning it stays on the same page
        self.assertIn(b"email already registered", response.data)  # Check if the error message is in the response

if __name__ == '__main__':
    unittest.main()
