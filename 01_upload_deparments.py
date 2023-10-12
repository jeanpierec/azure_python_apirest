import requests

# Define API URL departments
upload_csv_url_departments = "http://localhost:5000/upload-csv-departments"

# Replace database credentials
db_host = 'localhost'
db_name = 'airflow'
db_user = 'airflow'
db_password = 'airflow'

# Specify path to your departments file
departments_csv_path = 'data/departments.csv'

# Set the environment variables
import os
os.environ['DB_HOST'] = db_host
os.environ['DB_NAME'] = db_name
os.environ['DB_USER'] = db_user
os.environ['DB_PASSWORD'] = db_password

# Create a dictionary with the file to be uploaded
files = {'file': (departments_csv_path, open(departments_csv_path, 'rb'))}

# POST request for CSV file for departments
response = requests.post(upload_csv_url_departments, files=files)

# Print response
print(response.status_code)
print(response.json())
