import psycopg2
from flask import Blueprint, request, jsonify

book_routes = Blueprint('books', __name__)

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="fm",
    user="fm",
    password="fm"
)


@book_routes.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    authors_id = data.get('authors_id')
    book = {
        "publication_date": data.get('publication_date'),
        "name": data.get('name'),
        "category": data.get('category'),
        "quantity": data.get('quantity'),
        "aisle": data.get('aisle'),
        "shelf": data.get('shelf'),
        "position": data.get('position')
    }

    cur = conn.cursor()
    cur.execute("INSERT INTO books (publication_date, name, category, quantity, aisle, shelf, position) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (book["publication_date"], book["name"], book["category"],
                 book["quantity"], book["aisle"], book["shelf"], book["position"]))
    book_id = cur.fetchone()[0]

    for author_id in authors_id:
        cur.execute("INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)", (book_id, author_id))

    conn.commit()
    cur.close()

    return "Book created", 201


@book_routes.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = {
        "id": book_id,
        "publication_date": data.get('publication_date'),
        "name": data.get('name'),
        "category": data.get('category'),
        "quantity": data.get('quantity'),
        "aisle": data.get('aisle'),
        "shelf": data.get('shelf'),
        "position": data.get('position')
    }

    cur = conn.cursor()
    cur.execute("UPDATE books SET publication_date = %s, name = %s, category = %s, "
                "quantity = %s, aisle = %s, shelf = %s, position = %s WHERE id = %s",
                (book["publication_date"], book["name"], book["category"],
                 book["quantity"], book["aisle"], book["shelf"], book["position"], book_id))
    conn.commit()
    cur.close()

    return "Book updated", 200


@book_routes.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM book_authors WHERE book_id = %s", (book_id,))
    cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cur.close()

    return "Book deleted", 200


@book_routes.route('/books', methods=['GET'])
def get_books():
    cur = conn.cursor()
    cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    cur.close()

    return jsonify(books)


@book_routes.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cur.fetchone()
    cur.close()

    if book:
        return jsonify(book)
    else:
        return "Book not found", 404
