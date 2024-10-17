"""
This program runs tests for the profile management page
"""

import unittest
from flask import Flask
from app import app, database

class ProfileManagementTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Ensure there's a mock user in the database to test with
        self.existing_user = 'johndoe@gmail.com'
        database[self.existing_user] = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': self.existing_user,
            'password': 'password123'
        }

    # Test case for successful profile update
    def test_successful_profile_update(self):
        response = self.app.post(f'/profile/{self.existing_user}', data={
            'firstName': 'Johnny',
            'lastName': 'Doe',
            'email': 'johnnydoe@gmail.com',
            'password': 'newpassword123',
            'confirmPass': 'newpassword123',
            'action': 'Save Changes'
        })
        self.assertEqual(response.status_code, 302)  # Expect redirection on success
        self.assertEqual(database[self.existing_user]['firstName'], 'Johnny')
        self.assertEqual(database[self.existing_user]['email'], 'johnnydoe@gmail.com')
        self.assertEqual(database[self.existing_user]['password'], 'newpassword123')

    # Test case for when passwords do not match
    def test_password_mismatch(self):
        response = self.app.post(f'/profile/{self.existing_user}', data={
            'firstName': 'Johnny',
            'lastName': 'Doe',
            'email': 'johnnydoe@gmail.com',
            'password': 'newpassword123',
            'confirmPass': 'wrongpassword123',
            'action': 'Save Changes'
        })
        self.assertEqual(response.status_code, 200)  # Expect 200 OK, meaning it stays on the same page
        self.assertIn(b"Passwords do not match", response.data)

    # Test case for missing fields (empty email)
    def test_missing_field(self):
        response = self.app.post(f'/profile/{self.existing_user}', data={
            'firstName': 'Johnny',
            'lastName': 'Doe',
            'email': '',
            'password': 'newpassword123',
            'confirmPass': 'newpassword123',
            'action': 'Save Changes'
        })
        self.assertEqual(response.status_code, 200)  # Expect 200 OK, meaning it stays on the same page
        self.assertIn(b"All fields must be filled", response.data)

    # Test case for discarding changes
    def test_discard_changes(self):
        response = self.app.post(f'/profile/{self.existing_user}', data={
            'firstName': 'Johnny',
            'lastName': 'Doe',
            'email': 'johnnydoe@gmail.com',
            'password': 'newpassword123',
            'confirmPass': 'newpassword123',
            'action': 'Discard Changes'
        })
        self.assertEqual(response.status_code, 302)  # Expect redirection on discard
        self.assertEqual(database[self.existing_user]['firstName'], 'John')  # No changes should be made

if __name__ == '__main__':
    unittest.main()