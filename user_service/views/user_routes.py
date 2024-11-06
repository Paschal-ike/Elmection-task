from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from controllers.user_controller import create_user, get_all_users, get_user_by_email, update_user
import bcrypt

user_bp = Blueprint('users', __name__)

# Route to register a new user
@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Invalid input. Username, email, and password are required."}), 400

        # Check if user already exists
        existing_user = get_user_by_email(data['email'])
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 400

        # Hash the password before saving it
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Create new user
        user = create_user(data['username'], data['email'], hashed_password)

        # Generate JWT token for the user
        access_token = create_access_token(identity=user['email'])

        return jsonify({"message": "User created successfully", "access_token": access_token}), 201
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to log in an existing user and receive a token
@user_bp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required."}), 400

        # Check if the user exists
        user = get_user_by_email(data['email'])
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Check if the password is correct
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            return jsonify({"error": "Incorrect password"}), 401

        # Generate JWT token
        access_token = create_access_token(identity=user['email'])

        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to get all users (protected with JWT)
@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to get a specific user by email (protected with JWT)
@user_bp.route('/<string:email>', methods=['GET'])
@jwt_required()
def get_user(email):
    try:
        user = get_user_by_email(email)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to create a new user (protected with JWT)
@user_bp.route('/', methods=['POST'])
@jwt_required()
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
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to update an existing user (protected with JWT)
@user_bp.route('/<string:user_id>', methods=['PATCH'])
@jwt_required()
def update_user_route(user_id):
    try:
        data = request.get_json()
        user = update_user(user_id, data)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
