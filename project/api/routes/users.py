from flask import Blueprint, request, jsonify
from models import get_connection
import uuid
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users', __name__)

# GET ALL USERS
@users_bp.route('/users', methods=['GET'])
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, email, username, created_at FROM users;")
    users = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for user in users:
        result.append({
            "id": str(user[0]),
            "email": user[1],
            "username": user[2],
            "created_at": str(user[3])
        })

    return jsonify(result), 200


# CREATE USER (REGISTER)
@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # validation
    if not email or not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # check duplicate email
    cur.execute("SELECT id FROM users WHERE email=%s;", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        conn.close()
        return jsonify({"error": "Email already exists"}), 409

    hashed_password = generate_password_hash(password)

    user_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO users (id, email, username, password)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (user_id, email, username, hashed_password))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "User created",
        "id": user_id
    }), 201


# UPDATE USER
@users_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []

    if email:
        fields.append("email=%s")
        values.append(email)

    if username:
        fields.append("username=%s")
        values.append(username)

    if password:
        hashed_password = generate_password_hash(password)
        fields.append("password=%s")
        values.append(hashed_password)

    if not fields:
        return jsonify({"error": "No fields to update"}), 400

    values.append(id)

    query = f"UPDATE users SET {', '.join(fields)} WHERE id=%s;"

    cur.execute(query, values)

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User updated"}), 200


# DELETE USER
@users_bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=%s;", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User deleted"}), 200