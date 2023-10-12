FROM python:3.10

# Install the required Python libraries
RUN pip install Flask psycopg2 pandas pyodbc

# Copy the Python code to the Docker image
COPY . /usr/src/app

# Set the working directory
WORKDIR /usr/src/app

# Expose port 5000
EXPOSE 5000

# Start the Flask application
CMD ["python", "api_app_azure.py"]
