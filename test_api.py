import os
import unittest
from flask import Flask
from api_app import app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_upload_csv_departments(self):
        # Test the upload CSV for departments endpoint
        csv_path = os.path.join('data', 'test', 'departments.csv')
        with open(csv_path, 'rb') as csv_file:
            response = self.app.post('/upload-csv-departments', data={'file': (csv_file, 'departments.csv')})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data uploaded to departments successfully', response.data)

    def test_upload_csv_jobs(self):
        # Test the upload CSV for jobs endpoint
        csv_path = os.path.join('data', 'test', 'jobs.csv')
        with open(csv_path, 'rb') as csv_file:
            response = self.app.post('/upload-csv-jobs', data={'file': (csv_file, 'jobs.csv')})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data uploaded to jobs successfully', response.data)

    def test_upload_csv_hired_employees(self):
        # Test the upload CSV for hired employees endpoint
        csv_path = os.path.join('data', 'test', 'hired_employees.csv')
        with open(csv_path, 'rb') as csv_file:
            response = self.app.post('/upload-csv-hired-employees', data={'file': (csv_file, 'hired_employees.csv')})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data uploaded to hired employees successfully', response.data)

    # Add other test methods for your endpoints as needed