import psycopg2
from flask import Blueprint, request, jsonify

employee_routes = Blueprint('employees', __name__)

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="fm",
    user="fm",
    password="fm"
)


@employee_routes.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    employee = {
        "name": data.get('name'),
        "surname": data.get('surname'),
        "phone_number": data.get('phone_number')
    }

    cur = conn.cursor()
    cur.execute("INSERT INTO employees (name, surname, phone_number) VALUES (%s, %s, %s)",
                (employee["name"], employee["surname"], employee["phone_number"]))
    conn.commit()
    cur.close()

    return "Employee created", 201


@employee_routes.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    employee = {
        "id": employee_id,
        "name": data.get('name'),
        "surname": data.get('surname'),
        "phone_number": data.get('phone_number')
    }

    cur = conn.cursor()
    cur.execute("UPDATE employees SET name = %s, surname = %s, phone_number = %s WHERE id = %s",
                (employee["name"], employee["surname"], employee["phone_number"], employee_id))
    conn.commit()
    cur.close()

    return "Employee updated", 200


@employee_routes.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
    conn.commit()
    cur.close()

    return "Employee deleted", 200


@employee_routes.route('/employees', methods=['GET'])
def get_employees():
    cur = conn.cursor()
    cur.execute('SELECT * FROM employees')
    employees = cur.fetchall()
    cur.close()

    return jsonify(employees)
