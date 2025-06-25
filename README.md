# Taste Town Backened

Welcome to Taste Town, the backend powerhouse for a vibrant and efficient supermarket management system. Built with Flask, PostgreSQL, and secure token-based authentication, this API supports product inventory, user management, orders, and more—everything needed to run a modern digital market.

## Requirements
   -Framework: Use Flask to build a RESTful API.
   -Database: Use SQLite or PostgreSQL for data persistence.
   -API Features: Implement the following features/ endpoints:
    -User Management:
        -POST /api/register: Register a new user (store username, hashed password, email).
        -POST /api/login: Authenticate a user and return a JWT.
        -GET /api/profile: Retrieve authenticated user’s profile (protected route).
        -PUT /api/profile: Update user profile (e.g., name, email).

## Setup

### Pre-Requisites
    -Operating System: (Windows 10+, Linux 3.8+, or MacOS X 10.7+)
    -Python version: 3.12+
    -PostgreSQL (ensure a database is created)
    -Pipenv
    -RAM: 2GB minimum, 4GB recommended (for smoother development)
    -Free Disk Space: 1GB minimum, 2GB recommended


## Installation 

GitHub Repository:
### 1. Clone this repository
    git@github.com:BROM-town-squarebrom-e-commerce-backend.git

### 2. Navigate to project directory:
    cd brom-properties-backened

### 3. Install dependencies:
    pipenv shell

### 4. Activate python environment
    pipenv shell

### 5. Run migrations 
    flask db init (Run flask db init only once, and only if the migrations/ folder does not already exist)
    flask db migrate -m "Initial"
    flask db upgrade


## Project Structure
.
taste-town-backend/
│
├── server/
│   ├── models/
        |-- __init__.py
        |-- admin.py
│   ├── controllers/
│   ├── app.py
│   ├── config.py
│   └── seed.py
│
├── migrations/
├── requirements.txt
└── README.md

## Features
### User Management
| Method | Endpoint        | Description                    |
| ------ | --------------- | ------------------------------ |
| POST   | `/api/register` | Register a new user            |
| POST   | `/api/login`    | Authenticate user, return JWT  |
| GET    | `/api/profile`  | Get authenticated user profile |
| PUT    | `/api/profile`  | Update user profile            |
| POST   | `/api/refresh`  | Refresh JWT                    |


### Task Management
| Method | Endpoint          | Description                         |
| ------ | ----------------- | ----------------------------------- |
| POST   | `/api/tasks`      | Create a task                       |
| GET    | `/api/tasks`      | List all tasks (authenticated user) |
| PUT    | `/api/tasks/<id>` | Update a task                       |
| DELETE | `/api/tasks/<id>` | Delete a task                       |


### Item Catalog
| Method | Endpoint          | Description                         |
| ------ | ----------------- | ----------------------------------- |
| POST   | `/api/items`      | Create an item                      |
| GET    | `/api/items`      | List all items (optional filtering) |
| PUT    | `/api/items/<id>` | Update an item                      |
| DELETE | `/api/items/<id>` | Delete an item                      |


### Comment System
| Method | Endpoint                  | Description                           |
| ------ | ------------------------- | ------------------------------------- |
| POST   | `/api/comments`           | Add a comment to an item              |
| GET    | `/api/comments/<item_id>` | Get comments for a specific item      |
| DELETE | `/api/comments/<id>`      | Delete a comment (by author or admin) |


### Search
| Method | Endpoint      | Description                      |
| ------ | ------------- | -------------------------------- |
| GET    | `/api/search` | Search items or tasks by keyword |
