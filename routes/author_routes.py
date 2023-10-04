import psycopg2
from flask import Blueprint, request, jsonify

author_routes = Blueprint('db', __name__)

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="fm",
    user="fm",
    password="fm"
)


@author_routes.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    cur = conn.cursor()
    cur.execute("INSERT INTO authors (name, surname) VALUES (%s, %s)", (data.get('name'), data.get('surname')))
    conn.commit()
    cur.close()
    return "Author created", 201


@author_routes.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    data = request.get_json()
    cur = conn.cursor()
    cur.execute("UPDATE authors SET name = %s, surname = %s WHERE id = %s",
                (data.get('name'), data.get('surname'), author_id))
    conn.commit()
    cur.close()
    return "Author updated", 200


@author_routes.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id IN (SELECT book_id FROM book_authors WHERE author_id = %s)",
                (author_id,))
    cur.execute("DELETE FROM authors WHERE id = %s", (author_id,))
    cur.execute("DELETE FROM book_authors WHERE author_id = %s", (author_id,))
    conn.commit()
    cur.close()
    return "Author deleted", 200


@author_routes.route('/authors', methods=['GET'])
def get_authors():
    cur = conn.cursor()
    cur.execute('SELECT * FROM authors')
    authors = cur.fetchall()
    cur.close()
    return jsonify(authors)
