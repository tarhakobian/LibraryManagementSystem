import psycopg2
from flask import Blueprint, request, jsonify

rental_routes = Blueprint('rentals', __name__)

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="fm",
    user="fm",
    password="fm"
)


@rental_routes.route('/rentals', methods=['POST'])
def create_rental():
    data = request.get_json()
    rent = {
        "book_id": data.get('book_id'),
        "employee_id": data.get('employee_id'),
        "customer_id": data.get('customer_id'),
        "rent_date": data.get('rent_date'),
        "deadline": data.get('deadline'),
        "returned": data.get('returned')
    }

    cur = conn.cursor()
    cur.execute("INSERT INTO rent (book_id, employee_id, customer_id, rent_date, deadline, returned) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (rent["book_id"], rent["employee_id"], rent["customer_id"],
                 rent["rent_date"], rent["deadline"], rent["returned"]))

    cur.execute("UPDATE books SET quantity = quantity - 1 WHERE id = %s", (rent["book_id"]))

    conn.commit()
    cur.close()

    return "Rental created", 201


@rental_routes.route('/rentals/<int:rental_id>', methods=['PUT'])
def update_returned_rental(rental_id):
    cur = conn.cursor()
    cur.execute("UPDATE rent SET returned = true WHERE id = %s", (rental_id))

    # Get the book_id of the returned rental
    cur.execute("SELECT book_id FROM rent WHERE id = %s", (rental_id))
    book_id = cur.fetchone()[0]

    # Increase the book quantity when the rental is returned
    cur.execute("UPDATE books SET quantity = quantity + 1 WHERE id = %s", (book_id))

    conn.commit()
    cur.close()

    return "Rental marked as returned", 200


@rental_routes.route('/rentals/<int:rental_id>', methods=['DELETE'])
def delete_rental(rental_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM rent WHERE id = %s", (rental_id))
    conn.commit()
    cur.close()

    return "Rental deleted", 200


@rental_routes.route('/rentals', methods=['GET'])
def get_rentals():
    cur = conn.cursor()
    cur.execute('SELECT * FROM rent')
    rentals = cur.fetchall()
    cur.close()

    return jsonify(rentals)
