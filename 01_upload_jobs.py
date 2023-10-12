import requests

# API URL for jobs
upload_csv_url_jobs = "http://localhost:5000/upload-csv-jobs"

# Database credentials
db_host = 'localhost'
db_name = 'airflow'
db_user = 'airflow'
db_password = 'airflow'

# Specify pathjobs CSV file
jobs_csv_path = 'data/jobs.csv'

# Set the environment variables
import os
os.environ['DB_HOST'] = db_host
os.environ['DB_NAME'] = db_name
os.environ['DB_USER'] = db_user
os.environ['DB_PASSWORD'] = db_password

# Create a dictionary with the file
files = {'file': (jobs_csv_path, open(jobs_csv_path, 'rb'))}

# Make a POST request
response = requests.post(upload_csv_url_jobs, files=files)

# Print response
print(response.status_code)
print(response.json())
