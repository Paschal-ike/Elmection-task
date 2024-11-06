from app import mongo
from bson.objectid import ObjectId

# Function to retrieve all tasks
def get_all_tasks():
    tasks = mongo.db.tasks.find()  # Query the tasks collection
    result = []
    for task in tasks:
        result.append({
            'id': str(task['_id']),  # Convert ObjectId to string for the API response
            'title': task['title'],
            'description': task['description'],
            'completed': task['completed']
        })
    return result

# Function to retrieve a task by its ID
def get_task_by_id(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})  # Find task by ObjectId
    if task:
        return {
            'id': str(task['_id']),
            'title': task['title'],
            'description': task['description'],
            'completed': task['completed']
        }
    return None

# Function to create a new task
def create_task(title, description):
    task = {
        'title': title,
        'description': description,
        'completed': False  # Default value for the completed field
    }
    task_id = mongo.db.tasks.insert_one(task).inserted_id  # Insert task into MongoDB
    return {
        'id': str(task_id),
        'title': title,
        'description': description,
        'completed': False
    }

# Function to update an existing task
def update_task(task_id, data):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        updated_task = {}
        if 'title' in data:
            updated_task['title'] = data['title']
        if 'description' in data:
            updated_task['description'] = data['description']
        if 'completed' in data:
            updated_task['completed'] = data['completed']
        
        # Update the task in MongoDB
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': updated_task})
        
        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})  # Fetch the updated task
        return {
            'id': str(task['_id']),
            'title': task['title'],
            'description': task['description'],
            'completed': task['completed']
        }
    return None
