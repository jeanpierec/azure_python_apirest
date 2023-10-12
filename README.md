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