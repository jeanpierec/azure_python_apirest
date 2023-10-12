import requests

# Define the API URL for hired employees
upload_csv_url_hired_employees = "http://localhost:5000/upload-csv-hired-employees"

# Replace these placeholders with your database credentials
db_host = 'localhost'
db_name = 'airflow'
db_user = 'airflow'
db_password = 'airflow'

# Specify the path to your jobs CSV file
hired_employees_csv_path = 'data/hired_employees.csv'

# Set the environment variables for database credentials
import os
os.environ['DB_HOST'] = db_host
os.environ['DB_NAME'] = db_name
os.environ['DB_USER'] = db_user
os.environ['DB_PASSWORD'] = db_password

# Create a dictionary with the file to be uploaded
files = {'file': (hired_employees_csv_path, open(hired_employees_csv_path, 'rb'))}

# Make a POST request to upload the CSV file for hired employees
response = requests.post(upload_csv_url_hired_employees, files=files)

# Print the response
print(response.status_code)
print(response.json())