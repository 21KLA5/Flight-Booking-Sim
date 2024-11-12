import coverage
import unittest
from app import app, users_collection, bookings_collection

class LogInTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        users_collection.delete_many({})
        bookings_collection.delete_many({})
    
    def test_login_success(self):
        users_collection.insert_one({
            'firstName': 'Terence',
            'lastName': 'Jiang',
            'email': 'terencejiang@gmail.com',
            'password': 'password123'
        })

        response = self.app.post('/login', data={
            'email': 'terencejiang@gmail.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.location)

    def test_login_incorrect_password(self):
        users_collection.insert_one({
            'firstName': 'Jack',
            'lastName': 'Cam',
            'email': 'jackcam@gmail.com',
            'password': 'password123'
        })

        response = self.app.post('/login', data={
            'email': 'jackcam@gmail.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email and password does not match', response.data)

    def test_login_unregistered_email(self):
        response = self.app.post('/login', data={
            'email': 'nonexistent@gmail.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The provided email is not registered', response.data)

    def test_booking_history_without_login(self):
        response = self.app.get('/booking-history')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_booking_history_with_login(self):
        users_collection.insert_one({
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test@test.com',
            'password': 'test123'
        })
        
        with self.app as client:
            client.post('/login', data={
                'email': 'test@test.com',
                'password': 'test123'
            })
            
            bookings_collection.insert_one({
                "user_email": "test@test.com",
                "departureSeat": "A1",
                "returnSeat": "B1",
                "trip_type": "round_trip",
                "to_city": "London",
                "from_city": "Paris"
            })
            
            response = client.get('/booking-history')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'London', response.data)
            self.assertIn(b'Paris', response.data)

    def test_booking_history_empty(self):
        users_collection.insert_one({
            'firstName': 'Empty',
            'lastName': 'User',
            'email': 'empty@test.com',
            'password': 'test123'
        })
        
        with self.app as client:
            client.post('/login', data={
                'email': 'empty@test.com',
                'password': 'test123'
            })
            
            response = client.get('/booking-history')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        users_collection.delete_many({})
        bookings_collection.delete_many({})

def run_tests_with_coverage():
    cov = coverage.Coverage(
        branch=True,
        source=['app'],
        omit=[
            '*/tests/*',
            '*/venv/*',
            '*/env/*'
        ]
    )
    
    cov.start()
    suite = unittest.TestLoader().loadTestsFromTestCase(LogInTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    cov.stop()
    
    print("\nCoverage Summary:")
    cov.save()
    cov.report()
    
    return result

if __name__ == '__main__':
    run_tests_with_coverage()