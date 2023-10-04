import psycopg2
from flask import Blueprint, request, jsonify

customer_routes = Blueprint('customers', __name__)

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="fm",
    user="fm",
    password="fm"
)


@customer_routes.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = {
        "name": data.get('name'),
        "surname": data.get('surname'),
        "phone_number": data.get('phone_number')
    }

    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name, surname, phone_number) VALUES (%s, %s, %s)",
                (customer["name"], customer["surname"], customer["phone_number"]))
    conn.commit()
    cur.close()

    return "Customer created", 201


@customer_routes.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer = {
        "id": customer_id,
        "name": data.get('name'),
        "surname": data.get('surname'),
        "phone_number": data.get('phone_number')
    }

    cur = conn.cursor()
    cur.execute("UPDATE customers SET name = %s, surname = %s, phone_number = %s WHERE id = %s",
                (customer["name"], customer["surname"], customer["phone_number"], customer_id))
    conn.commit()
    cur.close()

    return "Customer updated", 200


@customer_routes.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
    conn.commit()
    cur.close()

    return "Customer deleted", 200


@customer_routes.route('/customers', methods=['GET'])
def get_customers():
    cur = conn.cursor()
    cur.execute('SELECT * FROM customers')
    customers = cur.fetchall()
    cur.close()

    return jsonify(customers)
