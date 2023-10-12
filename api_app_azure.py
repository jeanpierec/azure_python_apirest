import os
import csv
import psycopg2
from flask import Flask, request, jsonify
import pyodbc

# Create a Flask app
app = Flask(__name__)

def get_db_connection():
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=dataglobanttest.database.windows.net,1433;"
        "Database=globant;"
        "User=airflow@dataglobanttest;"
        "Password={secret_key};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    conn = pyodbc.connect(connection_string)

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

@app.route('/metrics/employees-hired-by-quarter', methods=['GET'])
def employees_hired_by_quarter():
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to calculate the number of employees hired for each job and department in 2021
    sql_query = """
    SELECT
        tb3.department,
        tb2.job,
        SUM(CASE
            WHEN EXTRACT(quarter FROM TO_DATE(datetime, 'YYYY-MM-DD')) = 1 THEN 1
            ELSE 0
        END) AS Q1,
        SUM(CASE
            WHEN EXTRACT(quarter FROM TO_DATE(datetime, 'YYYY-MM-DD')) = 2 THEN 1
            ELSE 0
        END) AS Q2,
        SUM(CASE
            WHEN EXTRACT(quarter FROM TO_DATE(datetime, 'YYYY-MM-DD')) = 3 THEN 1
            ELSE 0
        END) AS Q3,
        SUM(CASE
            WHEN EXTRACT(quarter FROM TO_DATE(datetime, 'YYYY-MM-DD')) = 4 THEN 1
            ELSE 0
        END) AS Q4
    FROM globant.hired_employees tb1
    INNER JOIN globant.jobs tb2 ON CAST(tb1.id AS VARCHAR) = CAST(tb2.id AS VARCHAR)
    INNER JOIN globant.departments tb3 ON CAST(tb1.department_id AS VARCHAR)= CAST(tb3.id AS VARCHAR)
    WHERE TO_DATE(datetime, 'YYYY-MM-DD') >= '2021-01-01' AND TO_DATE(datetime, 'YYYY-MM-DD') <= '2021-12-31'
    GROUP BY tb3.department, tb2.job
    ORDER BY tb3.department, tb2.job;
    """
    
    cursor.execute(sql_query)
    data = cursor.fetchall()
    
    conn.close()
    
    # Convert the data to a list of dictionaries
    result = [{'department': row[0], 'job': row[1], 'Q1': row[2], 'Q2': row[3], 'Q3': row[4], 'Q4': row[5]} for row in data]

    return jsonify(result)

@app.route('/metrics/departments-hiring-more-than-mean', methods=['GET'])
def departments_hiring_more_than_mean():
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to calculate the mean number of employees hired in 2021
    mean_query = """
    SELECT AVG(employees_hired) FROM (
        SELECT department_id, COUNT(*) AS employees_hired
        FROM globant.hired_employees
        WHERE TO_DATE(datetime, 'YYYY-MM-DD') >= '2021-01-01' AND TO_DATE(datetime, 'YYYY-MM-DD') <= '2021-12-31'
        GROUP BY department_id
    ) AS hire_counts;
    """

    cursor.execute(mean_query)
    mean_result = cursor.fetchone()[0]

    # SQL query to fetch departments hiring more employees than the mean
    departments_query = """
    SELECT departments.id, departments.department, hire_counts.employees_hired
    FROM (
        SELECT department_id, COUNT(*) AS employees_hired
        FROM globant.hired_employees
        WHERE TO_DATE(datetime, 'YYYY-MM-DD') >= '2021-01-01' AND TO_DATE(datetime, 'YYYY-MM-DD') <= '2021-12-31'
        GROUP BY department_id
    ) AS hire_counts
    INNER JOIN globant.departments ON CAST(hire_counts.department_id AS varchar) = CAST(departments.id AS varchar)
    WHERE hire_counts.employees_hired > %s
    ORDER BY hire_counts.employees_hired DESC;
    """

    cursor.execute(departments_query, (mean_result,))
    data = cursor.fetchall()

    conn.close()

    # Convert the data to a list of dictionaries
    result = [{'id': row[0], 'department': row[1], 'employees_hired': row[2]} for row in data]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
