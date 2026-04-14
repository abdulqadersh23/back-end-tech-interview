from flask import Blueprint, request, jsonify
from models import get_connection
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)


# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    #  
    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, email, username, password
        FROM users
        WHERE email=%s;
    """, (email,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    # user not found
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user[0]
    user_email = user[1]
    user_username = user[2]
    hashed_password = user[3]

    # password check
    if not check_password_hash(hashed_password, password):
        return jsonify({"error": "Invalid password"}), 401

    # create JWT token
    access_token = create_access_token(
        identity=str(user_id),
        additional_claims={
            "email": user_email,
            "username": user_username
        },
        expires_delta=timedelta(hours=1)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": str(user_id),
            "email": user_email,
            "username": user_username
        }
    }), 200