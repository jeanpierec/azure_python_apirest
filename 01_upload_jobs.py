import requests

# Define the API URL for jobs
upload_csv_url_jobs = "http://localhost:5000/upload-csv-jobs"

# Replace these placeholders with your database credentials
db_host = 'localhost'
db_name = 'airflow'
db_user = 'airflow'
db_password = 'airflow'

# Specify the path to your jobs CSV file
jobs_csv_path = 'data/jobs.csv'

# Set the environment variables for database credentials
import os
os.environ['DB_HOST'] = db_host
os.environ['DB_NAME'] = db_name
os.environ['DB_USER'] = db_user
os.environ['DB_PASSWORD'] = db_password

# Create a dictionary with the file to be uploaded
files = {'file': (jobs_csv_path, open(jobs_csv_path, 'rb'))}

# Make a POST request to upload the CSV file for jobs
response = requests.post(upload_csv_url_jobs, files=files)

# Print the response
print(response.status_code)
print(response.json())
