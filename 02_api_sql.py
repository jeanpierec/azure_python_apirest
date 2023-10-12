from flask import Flask, request, jsonify
import psycopg2
import os
import csv

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
