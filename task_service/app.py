from flask import Flask
from flask_pymongo import PyMongo
import os

# Initialize PyMongo for MongoDB interaction
mongo = PyMongo()

def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # MongoDB URI for the task service
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/task_db")

    # Initialize extensions
    mongo.init_app(app)

    # Import the task blueprint here to avoid circular import
    from views.task_routes import task_bp
    app.register_blueprint(task_bp, url_prefix='/tasks')

    return app

# Start the Flask app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
