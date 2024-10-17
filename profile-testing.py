import unittest
from app import app, database  # Import your app and database

class ProfileManagementTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Reset the database before each test
        self.existing_user = 'johndoe@gmail.com'
        database.clear()  # Clear previous entries in the mock database
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
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Expect 200 OK after redirection
        # Check if the new email key exists in the database
        self.assertIn('johnnydoe@gmail.com', database)
        self.assertEqual(database['johnnydoe@gmail.com']['firstName'], 'Johnny')
        self.assertEqual(database['johnnydoe@gmail.com']['email'], 'johnnydoe@gmail.com')
        self.assertEqual(database['johnnydoe@gmail.com']['password'], 'newpassword123')
        # Ensure the old email key no longer exists
        self.assertNotIn(self.existing_user, database)

    # Test case for when passwords do not match
    def test_password_mismatch(self):
        response = self.app.post(f'/profile/{self.existing_user}', data={
            'firstName': 'Johnny',
            'lastName': 'Doe',
            'email': 'johnnydoe@gmail.com',
            'password': 'newpassword123',
            'confirmPass': 'wrongpassword123',
            'action': 'Save Changes'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Expect 200 OK
        self.assertIn(b"Passwords do not match", response.data)
        # Ensure the database has not been altered
        self.assertEqual(database[self.existing_user]['firstName'], 'John')

    # Test case for missing fields (empty email)
    def test_missing_field(self):
        response = self.app.post(f'/profile/{self.existing_user}', data={
            'firstName': 'Johnny',
            'lastName': 'Doe',
            'email': '',
            'password': 'newpassword123',
            'confirmPass': 'newpassword123',
            'action': 'Save Changes'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Expect 200 OK
        self.assertIn(b"All fields must be filled.", response.data)
        # Ensure the database has not been altered
        self.assertEqual(database[self.existing_user]['firstName'], 'John')

    # Test case for discarding changes
    def test_discard_changes(self):
        response = self.app.post(f'/profile/{self.existing_user}', data={
            'firstName': 'Johnny',
            'lastName': 'Doe',
            'email': 'johnnydoe@gmail.com',
            'password': 'newpassword123',
            'confirmPass': 'newpassword123',
            'action': 'Discard Changes'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Expect 200 OK after redirection
        # Ensure no changes have been made
        self.assertEqual(database[self.existing_user]['firstName'], 'John')
        self.assertEqual(database[self.existing_user]['email'], 'johndoe@gmail.com')
        self.assertNotIn('johnnydoe@gmail.com', database)

if __name__ == '__main__':
    unittest.main()
