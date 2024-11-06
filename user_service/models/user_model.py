from app import mongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @classmethod
    def create_user(cls, username, email, password):
        # Check if the user already exists in the database
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            return {"error": "User already exists."}

   
        hashed_password = generate_password_hash(password)

        # Create the new user in the database
        user = {
            'username': username,
            'email': email,
            'password': hashed_password
        }

        # Insert the new user into the MongoDB database
        user_id = mongo.db.users.insert_one(user).inserted_id
        return {
            'id': str(user_id),
            'username': username,
            'email': email
        }

    @classmethod
    def get_all_users(cls):
        # Retrieve all users from the database
        users = mongo.db.users.find()
        result = []
        for user in users:
            result.append({
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email']
            })
        return result

    @classmethod
    def get_user_by_email(cls, email):
        # Retrieve a user by email from the database
        user = mongo.db.users.find_one({'email': email})
        if user:
            return {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email']
            }
        return None

    @classmethod
    def update_user(cls, user_id, data):
        # Find the user by ID
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

            # Fetch and return the updated user
            user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            return {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email']
            }
        return None

    @classmethod
    def authenticate_user(cls, email, password):
        # Find the user by email
        user = mongo.db.users.find_one({'email': email})
        if user:
          
            if check_password_hash(user['password'], password):
                return {"id": str(user['_id']), "username": user['username'], "email": user['email']}
        return {"error": "Invalid credentials."}
