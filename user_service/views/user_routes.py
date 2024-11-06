from flask import Blueprint, jsonify, request
from controllers.user_controller import create_user, get_all_users, get_user_by_email, update_user

user_bp = Blueprint('users', __name__)

# Route to get all users
@user_bp.route('/', methods=['GET'])
def get_users():
    try:
        users = get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# Route to get a specific user by email
@user_bp.route('/<string:email>', methods=['GET'])
def get_user(email):
    try:
        user = get_user_by_email(email)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# Route to create a new user
@user_bp.route('/', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Invalid input. Username, email, and password are required."}), 400
        user = create_user(data['username'], data['email'], data['password'])
        if "error" in user:
            return jsonify(user), 400
        return jsonify(user), 201
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# Route to update an existing user
@user_bp.route('/<string:user_id>', methods=['PATCH'])
def update_user_route(user_id):
    try:
        data = request.get_json()
        user = update_user(user_id, data)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
