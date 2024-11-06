# Microservices Overview

This project contains two microservices built using Flask:

1. **User Service**: Manages user data and authentication.
2. **Task Service**: Manages tasks for users.

## Overview

- **User Service** handles:
  - User registration, login, and authentication.
  - Retrieving, updating, and deleting users.
  
- **Task Service** handles:
  - Task management (creating, retrieving, and updating tasks).
  - Authentication for users to perform tasks.

Both services are backed by a MongoDB database and communicate with each other using Docker Compose for container orchestration.

## Services

### 1. User Service

The **User Service** manages user data and authentication. It provides endpoints for:

- **POST /users**: Create a new user.
- **GET /users/{email}**: Get user details by email.
- **GET /users**: Get all users.
- **PATCH /users/{user_id}**: Update user information.
- **POST /login**: Authenticate user and get a JWT token.

#### Key Features:
- User registration and login.
- JWT-based token authentication.
- CRUD operations for users (Create, Read, Update, Delete).

#### Environment Variables:
- `FLASK_APP=app.py`
- `MONGO_URI=mongodb://mongo:27017/user_db`

### 2. Task Service

The **Task Service** manages tasks and user-task associations. It provides endpoints for:

- **POST /tasks**: Create a new task.
- **GET /tasks/{task_id}**: Retrieve task details by ID.
- **GET /tasks**: Retrieve all tasks.
- **PATCH /tasks/{task_id}**: Update task details.

#### Key Features:
- Task creation and management.
- CRUD operations for tasks (Create, Read, Update, Delete).
- Authentication for users to interact with tasks.

#### Environment Variables:
- `FLASK_APP=app.py`
- `MONGO_URI=mongodb://mongo:27017/task_db`

### 3. MongoDB

Both services use a shared **MongoDB** instance for data storage. MongoDB is set up in a Docker container and is accessible through the `mongo` service.

#### Mongo Environment Variables:
- `MONGO_URI=mongodb://mongo:27017/<db_name>` (for both user and task databases)

## Getting Started

### Prerequisites
- Docker and Docker Compose installed.

### Running the Services

Clone the repository to your local machine.
   
   ```bash
   git clone <repository-url>
   cd <repository-folder>
