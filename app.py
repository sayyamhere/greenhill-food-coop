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


@app.route("/members", methods=["GET"])
def get_members():
    connection = get_db_connection()

    members = connection.execute(
        "SELECT * FROM members"
    ).fetchall()

    connection.close()

    return jsonify([dict(member) for member in members])


@app.route("/members", methods=["POST"])
def add_member():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    connection = get_db_connection()

    connection.execute(
        "INSERT INTO members (name, email) VALUES (?, ?)",
        (name, email)
    )

    connection.commit()
    connection.close()

    return jsonify({"message": "Member added successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)