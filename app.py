from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "greenhill.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return "Greenhill Food Co-op Ordering System"


@app.route("/products", methods=["GET"])
def get_products():
    connection = get_db_connection()

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    return jsonify([dict(product) for product in products])


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock", 0)

    if not name or price is None:
        return jsonify({
            "error": "name and price are required"
        }), 400

    connection = get_db_connection()

    connection.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product added successfully"
    }), 201


if __name__ == "__main__":
    app.run(debug=True)