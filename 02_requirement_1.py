import requests

# Define the API URL for the "Number of employees hired for each job and department in 2021 divided by quarter" endpoint
metrics_url_1 = "http://localhost:5000/metrics/employees-hired-by-quarter"

# Make a GET request to the endpoint
response = requests.get(metrics_url_1)

# Check the response status code and print the data
if response.status_code == 200:
    data = response.json()
    for item in data:
        print(f"Department: {item['department']}, Job: {item['job']}, Q1: {item['Q1']}, Q2: {item['Q2']}, Q3: {item['Q3']}, Q4: {item['Q4']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
