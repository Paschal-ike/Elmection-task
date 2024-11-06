from app import mongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import bcrypt

# Function to create a new user
def create_user(username, email, password):
    # Check if the user already exists
    existing_user = mongo.db.users.find_one({'email': email})
    if existing_user:
        return {"error": "User already exists."}

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create the user record
    user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }

    # Insert the new user into the database
    user_id = mongo.db.users.insert_one(user).inserted_id
    return {
        'id': str(user_id),
        'username': username,
        'email': email
    }

# Function to retrieve all users
def get_all_users():
    users = mongo.db.users.find()  # Query the users collection
    result = []
    for user in users:
        result.append({
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        })
    return result

# Function to retrieve a specific user by email
def get_user_by_email(email):
    user = mongo.db.users.find_one({'email': email})
    if user:
        return {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        }
    return None

# Function to update an existing user
def update_user(user_id, data):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        updated_user = {}
        if 'username' in data:
            updated_user['username'] = data['username']
        if 'email' in data:
            updated_user['email'] = data['email']
        if 'password' in data:
            updated_user['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())  # Hash the new password

        # Update the user in MongoDB
        mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})

        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})  # Fetch the updated user
        return {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        }
    return None

# Function to authenticate a user (Login)
def authenticate_user(email, password):
    # Find the user by email
    user = mongo.db.users.find_one({'email': email})
    if user:
        # Check if the provided password matches the hashed password in the database
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # Generate JWT token upon successful authentication
            access_token = create_access_token(identity=user['email'])
            return {"access_token": access_token}
    return {"error": "Invalid credentials."}
