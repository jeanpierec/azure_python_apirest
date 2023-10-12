# azure_python_apirest
## API Rest Python Challenge

This repository contains a API Flask app to upload a CSV file to a table database.

### Requirements

Please, red the <em>requirements.txt</em> for more information about the libraries.

## Section 01: API

We have this files:


1. 01_api_app.py: With the Flask Python App code.
2. 01_upload_deparments.py: For upload deparments CSV file.
3. 01_hired_employees.py: For upload hired employees CSV file.
4. 01_upload_jobss.py: For upload jobs CSV file.


For run the APP, first, we have to run <em>01_api_app.py</em> in a terminal instance:

> python 01_api_app.py

Now, you can upload all of each CSV in <em>data</em> folder. For this case, in another terminal we'll run:

> python upload_hired_employees.py
> python upload_deparments.py
> python upload_jobs.py

Now, you can use a DB explorer to cheack all tables.

## Section 02: Requirements

For every requirements I created a python script:

#### Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.

To see the result, you can execute the python file in a terminal (run de <em>api_app.py</em> before):

> python 02_requirement_1.py

#### List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

To see the result, you can execute the python file in a terminal (run de <em>api_app.py</em> before):

> python 02_requirement_2.py

## Bonus: Unit tests

I creadted unit tests for the principal function in the API: Upload the CSV file to DB. So, we can find in the python scripts <em>test_api.py</em> three test for the three function to upload CSV file for each table.

To run the test, run de <em>api_app.py</em> and then, run the test script:

> python -m unittest test_api

## Bonus: Deployment in Azure

We use Azure for deployment the App. See more in the PDF <em>"deployment_azure.pdf"</em> for more details.

> For this example we use api_app_azure.py with SQL Azure Server parameters

1. Create a Docker image (See <em>Dockerfile</em>) and upload the image to DockerHub.
2. In Azure, create a basic SQL Server (See more in the PDF <em>"deployment_azure.pdf"</em>).
3. In Azure, create a Kubernetes node (See more in the PDF <em>"deployment_azure.pdf"</em>).
4. Create a deployment file. In this case we use <em>kubectl.yaml</em>.
5. Deploying with Kubernetes on AKS (Azure Kubernetes Service). See more in the PDF <em>"deployment_azure.pdf"</em>.

### Conclusions

We could configure secret credentials for DB conexion for example.


#### Notes

In <em>evidences</em> folder you can see screenshots for all executions.