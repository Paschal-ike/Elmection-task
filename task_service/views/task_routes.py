from flask import Blueprint, jsonify, request
from controllers.task_controller import get_all_tasks, get_task_by_id, create_task, update_task

task_bp = Blueprint('tasks', __name__)

# Route to get all tasks
@task_bp.route('/', methods=['GET'])
def get_tasks():
    try:
        tasks = get_all_tasks()
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# Route to get a specific task by its ID
@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = get_task_by_id(task_id)
        if task:
            return jsonify(task), 200
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# Route to create a new task
@task_bp.route('/', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'description' not in data:
            return jsonify({"error": "Invalid input. Both title and description are required."}), 400
        task = create_task(data['title'], data['description'])
        return jsonify(task), 201
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# Route to update an existing task
@task_bp.route('/<int:task_id>', methods=['PATCH'])
def update_task_route(task_id):
    try:
        data = request.get_json()
        task = update_task(task_id, data)
        if task:
            return jsonify(task), 200
        return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
