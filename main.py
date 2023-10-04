from flask import Flask
from routes.author_routes import author_routes
from routes.book_routes import book_routes
from routes.customer_routes import customer_routes
from routes.employee_routes import employee_routes
from routes.rental_routes import rental_routes

app = Flask("Library")

# Register the blueprints
app.register_blueprint(author_routes, url_prefix='/db')
app.register_blueprint(book_routes, url_prefix='/books')
app.register_blueprint(customer_routes, url_prefix='/customers')
app.register_blueprint(employee_routes, url_prefix='/employees')
app.register_blueprint(rental_routes, url_prefix='/rentals')

if __name__ == '__main__':
    app.run(debug=True)
