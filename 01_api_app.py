import os
import csv
import psycopg2
from flask import Flask, request, jsonify

# Create a Flask app
app = Flask(__name__)

def get_db_connection():
    # PostgreSQL credentials
    # For the first exercise we'll use a local docker postgresql
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_name = os.environ.get('DB_NAME', 'airflow')
    db_user = os.environ.get('DB_USER', 'airflow')
    db_password = os.environ.get('DB_PASSWORD', 'airflow')

    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    return conn

def create_tables_if_not_exist():
    """
        Create SQL tables in Postgresql used a psyg2
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL Create tables
    # NOTICE: For Hired Employees table two id columns for job and deparment
    #         I've to change the data type beacuse we've null values.
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS globant;
        CREATE TABLE IF NOT EXISTS globant.departments (
            id integer,
            department varchar(255)
        );
        CREATE TABLE IF NOT EXISTS globant.jobs (
            id integer,
            job varchar(255)
        );
        CREATE TABLE IF NOT EXISTS globant.hired_employees (
            id integer,
            name varchar(255),
            datetime varchar(255),
            department_id varchar(4),
            job_id varchar(4)
        );
    """)

    conn.commit()
    conn.close()

@app.route('/upload-csv-departments', methods=['POST'])
def upload_csv_departments():
    """Upload CSV file for Deparments table

    Returns:
        status: HTTP 500 error if the file didn't upload. Otherwise, a finished message
    """
    create_tables_if_not_exist()

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            csv_data = csv.reader(file.stream.read().decode('utf-8').splitlines())

            for row in csv_data:
                cursor.execute("INSERT INTO globant.departments (id, department) VALUES (%s, %s)", (row[0],row[1],))

            conn.commit()
            conn.close()
            return jsonify({'message': 'Data uploaded to departments successfully'}), 200

        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'error': str(e)}), 500

@app.route('/upload-csv-jobs', methods=['POST'])
def upload_csv_jobs():
    """Upload CSV file for Jobs table

    Returns:
        status: HTTP 500 error if the file didn't upload. Otherwise, a finished message
    """
    create_tables_if_not_exist()

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            csv_data = csv.reader(file.stream.read().decode('utf-8').splitlines())

            for row in csv_data:
                cursor.execute("INSERT INTO globant.jobs (id,job) VALUES (%s,%s)", (row[0],row[1],))

            conn.commit()
            conn.close()
            return jsonify({'message': 'Data uploaded to jobs successfully'}), 200

        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'error': str(e)}), 500

@app.route('/upload-csv-hired-employees', methods=['POST'])
def upload_csv_hired_employees():
    """Upload CSV file for Hired employees table

    Returns:
        status: HTTP 500 error if the file didn't upload. Otherwise, a finished message
    """
    create_tables_if_not_exist()

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            csv_data = csv.reader(file.stream.read().decode('utf-8').splitlines())
            # next(csv_data) # If we want to skip the header

            for row in csv_data:
                cursor.execute("""
                    INSERT INTO globant.hired_employees (id, name, datetime, department_id, job_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (row[0], row[1], row[2], row[3], row[4]))

            conn.commit()
            conn.close()
            return jsonify({'message': 'Data uploaded to hired employees successfully'}), 200

        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
