import requests

# Define the API URL for the "List of ids, name, and number of employees hired by departments hiring more than the mean" endpoint
metrics_url_2 = "http://localhost:5000/metrics/departments-hiring-more-than-mean"

# Make a GET request to the endpoint
response = requests.get(metrics_url_2)

# Check the response status code and print the data
if response.status_code == 200:
    data = response.json()
    for item in data:
        print(f"ID: {item['id']}, Department: {item['department']}, Employees Hired: {item['employees_hired']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
