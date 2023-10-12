import requests

# Define the API URL for departments
upload_csv_url_departments = "http://localhost:5000/upload-csv-departments"

# Replace these placeholders with your database credentials
db_host = 'localhost'
db_name = 'airflow'
db_user = 'airflow'
db_password = 'airflow'

# Specify the path to your departments CSV file
departments_csv_path = 'data/departments.csv'

# Set the environment variables for database credentials
import os
os.environ['DB_HOST'] = db_host
os.environ['DB_NAME'] = db_name
os.environ['DB_USER'] = db_user
os.environ['DB_PASSWORD'] = db_password

# Create a dictionary with the file to be uploaded
files = {'file': (departments_csv_path, open(departments_csv_path, 'rb'))}

# Make a POST request to upload the CSV file for departments
response = requests.post(upload_csv_url_departments, files=files)

# Print the response
print(response.status_code)
print(response.json())
