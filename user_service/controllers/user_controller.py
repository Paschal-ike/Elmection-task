from app import mongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Function to create a new user
def create_user(username, email, password):
    # Check if the user already exists
    existing_user = mongo.db.users.find_one({'email': email})
    if existing_user:
        return {"error": "User already exists."}
    
    hashed_password = generate_password_hash(password)
    
    user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }
    
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
            updated_user['password'] = generate_password_hash(data['password'])  # Hash the new password
        
        # Update the user in MongoDB
        mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
        
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})  # Fetch the updated user
        return {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        }
    return None
