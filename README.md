# Task Manager API

A Django REST Framework-based API for managing tasks and user assignments. This project provides a robust API for creating, assigning, and tracking tasks with user management capabilities.

## Features

- Task Management (Create, Read, Update, Delete)
- User Assignment System
- Task Status Tracking
- Task Type Categorization
- API Documentation (Swagger/ReDoc)
- Admin Interface
- Comprehensive Test Suite

## Project Structure

```
TaskManager/              # Project root directory
├── taskmanager/         # Django project configuration
│   ├── settings.py     # Project settings
│   ├── urls.py         # Main URL routing
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
├── tasks/              # Django app directory
│   ├── api/           # API-specific code
│   │   ├── views.py   # View logic
│   │   ├── serializers.py  # Data serialization
│   │   └── urls.py    # App-specific URLs
│   ├── models.py      # Database models
│   ├── admin.py       # Admin interface
│   ├── tests/         # Test files
│   │   ├── test_models.py
│   │   ├── test_serializers.py
│   │   └── test_views.py
│   └── utils/         # Utility functions
├── manage.py          # Django management script
└── requirements.txt   # Project dependencies
```

## Setup Instructions

1. Create a virtual environment (Windows/Linux):
```bash
python -m venv venv
venv\Scripts\activate  # On Linux: source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

The API documentation is available in two formats:

1. Swagger UI: http://127.0.0.1:8000/swagger/
   - Interactive documentation
   - Try out API endpoints directly
   - View request/response schemas

2. ReDoc: http://127.0.0.1:8000/redoc/
   - Alternative documentation view
   - Clean, organized layout
   - Easy to read format

## API Endpoints

### Tasks

#### 1. List All Tasks
```http
GET /api/tasks/
Authorization: Basic <credentials>
```

Response:
```json
[
    {
        "id": 1,
        "name": "Complete Project Documentation",
        "description": "Write comprehensive documentation for the task management API",
        "created_at": "2024-03-20T10:00:00Z",
        "task_type": "documentation",
        "completed_at": null,
        "status": "pending",
        "assigned_to": [],
        "created_by": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User"
        }
    }
]
```

#### 2. Create a Task
```http
POST /api/tasks/
Content-Type: application/json
Authorization: Basic <credentials>

{
    "name": "Complete Project Documentation",
    "description": "Write comprehensive documentation for the task management API",
    "task_type": "documentation"
}
```

Response:
```json
{
    "id": 1,
    "name": "Complete Project Documentation",
    "description": "Write comprehensive documentation for the task management API",
    "created_at": "2024-03-20T10:00:00Z",
    "task_type": "documentation",
    "completed_at": null,
    "status": "pending",
    "assigned_to": [],
    "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User"
    }
}
```

#### 3. Get Task Details
```http
GET /api/tasks/1/
Authorization: Basic <credentials>
```

Response:
```json
{
    "id": 1,
    "name": "Complete Project Documentation",
    "description": "Write comprehensive documentation for the task management API",
    "created_at": "2024-03-20T10:00:00Z",
    "task_type": "documentation",
    "completed_at": null,
    "status": "pending",
    "assigned_to": [],
    "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User"
    }
}
```

#### 4. Update a Task
```http
PUT /api/tasks/1/
Content-Type: application/json
Authorization: Basic <credentials>

{
    "name": "Updated Task Name",
    "description": "Updated task description",
    "task_type": "development",
    "status": "in_progress"
}
```

Response:
```json
{
    "id": 1,
    "name": "Updated Task Name",
    "description": "Updated task description",
    "created_at": "2024-03-20T10:00:00Z",
    "task_type": "development",
    "completed_at": null,
    "status": "in_progress",
    "assigned_to": [],
    "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User"
    }
}
```

#### 5. Delete a Task
```http
DELETE /api/tasks/1/
Authorization: Basic <credentials>
```

Response:
```http
HTTP 204 No Content
```

### Users

#### 1. List All Users
```http
GET /api/users/
Authorization: Basic <credentials>
```

Response:
```json
[
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "is_staff": true,
        "is_active": true,
        "date_joined": "2024-03-20T10:00:00Z"
    },
    {
        "id": 2,
        "username": "testuser1",
        "email": "test1@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2024-03-20T11:00:00Z"
    }
]
```

#### 2. Create a User
```http
POST /api/users/
Content-Type: application/json
Authorization: Basic <credentials>

{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123",
    "first_name": "New",
    "last_name": "User"
}
```

Response:
```json
{
    "id": 3,
    "username": "newuser",
    "email": "newuser@example.com",
    "first_name": "New",
    "last_name": "User",
    "is_staff": false,
    "is_active": true,
    "date_joined": "2024-03-20T12:00:00Z"
}
```

#### 3. Get User Details
```http
GET /api/users/1/
Authorization: Basic <credentials>
```

Response:
```json
{
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_staff": true,
    "is_active": true,
    "date_joined": "2024-03-20T10:00:00Z"
}
```

#### 4. Update a User
```http
PUT /api/users/1/
Content-Type: application/json
Authorization: Basic <credentials>

{
    "first_name": "Updated",
    "last_name": "Name",
    "email": "updated@example.com"
}
```

Response:
```json
{
    "id": 1,
    "username": "admin",
    "email": "updated@example.com",
    "first_name": "Updated",
    "last_name": "Name",
    "is_staff": true,
    "is_active": true,
    "date_joined": "2024-03-20T10:00:00Z"
}
```

#### 5. Delete a User
```http
DELETE /api/users/1/
Authorization: Basic <credentials>
```

Response:
```http
HTTP 204 No Content
```

#### 6. Change User Password
```http
POST /api/users/1/change_password/
Content-Type: application/json
Authorization: Basic <credentials>

{
    "old_password": "currentpassword",
    "new_password": "newpassword123"
}
```

Response:
```json
{
    "detail": "Password successfully changed."
}
```

#### 7. Reset User Password
```http
POST /api/users/1/reset_password/
Content-Type: application/json
Authorization: Basic <credentials>

{
    "new_password": "newpassword123"
}
```

Response:
```json
{
    "detail": "Password successfully reset."
}
```

#### 8. Get User Profile
```http
GET /api/users/me/
Authorization: Basic <credentials>
```

Response:
```json
{
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "is_staff": true,
    "is_active": true,
    "date_joined": "2024-03-20T10:00:00Z"
}
```

#### 9. Update User Profile
```http
PUT /api/users/me/
Content-Type: application/json
Authorization: Basic <credentials>

{
    "first_name": "Updated",
    "last_name": "Name",
    "email": "updated@example.com"
}
```

Response:
```json
{
    "id": 1,
    "username": "admin",
    "email": "updated@example.com",
    "first_name": "Updated",
    "last_name": "Name",
    "is_staff": true,
    "is_active": true,
    "date_joined": "2024-03-20T10:00:00Z"
}
```

### Task Assignments

#### 1. Assign Users to a Task
```http
POST /api/tasks/1/assign/
Content-Type: application/json
Authorization: Basic <credentials>

{
    "user_ids": [1, 2]
}
```

Response:
```json
{
    "id": 1,
    "name": "Updated Task Name",
    "description": "Updated task description",
    "created_at": "2024-03-20T10:00:00Z",
    "task_type": "development",
    "completed_at": null,
    "status": "in_progress",
    "assigned_to": [
        {
            "id": 1,
            "username": "testuser1",
            "email": "test1@example.com",
            "first_name": "John",
            "last_name": "Doe"
        },
        {
            "id": 2,
            "username": "testuser2",
            "email": "test2@example.com",
            "first_name": "Jane",
            "last_name": "Smith"
        }
    ],
    "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User"
    }
}
```

#### 2. Get Task Assignments
```http
GET /api/tasks/1/assignments/
Authorization: Basic <credentials>
```

Response:
```json
[
    {
        "id": 1,
        "username": "testuser1",
        "email": "test1@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    {
        "id": 2,
        "username": "testuser2",
        "email": "test2@example.com",
        "first_name": "Jane",
        "last_name": "Smith"
    }
]
```

### User Tasks

#### 1. Get Tasks Assigned to a User
```http
GET /api/users/1/tasks/
Authorization: Basic <credentials>
```

Response:
```json
[
    {
        "id": 1,
        "name": "Updated Task Name",
        "description": "Updated task description",
        "created_at": "2024-03-20T10:00:00Z",
        "task_type": "development",
        "completed_at": null,
        "status": "in_progress",
        "assigned_to": [
            {
                "id": 1,
                "username": "testuser1",
                "email": "test1@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        ],
        "created_by": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User"
        }
    }
]
```

### Error Responses

#### 1. Authentication Error
```http
HTTP 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

#### 2. Permission Error
```http
HTTP 403 Forbidden
{
    "detail": "You do not have permission to perform this action."
}
```

#### 3. Not Found Error
```http
HTTP 404 Not Found
{
    "detail": "Not found."
}
```

#### 4. Validation Error
```http
HTTP 400 Bad Request
{
    "name": [
        "Task name must be at least 3 characters long."
    ],
    "task_type": [
        "Select a valid choice. That choice is not one of the available choices."
    ]
}
```

## Testing

### Running Tests

To run all tests:
```bash
python manage.py test
```

To run specific test files:
```bash
python manage.py test tasks.tests.test_models
python manage.py test tasks.tests.test_serializers
python manage.py test tasks.tests.test_views
```

To run tests with coverage report:
```bash
coverage run manage.py test
coverage report
```

### Test Credentials

The test suite uses the following test users:

1. Admin User:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `admin123`

2. Regular Users:
   - User 1:
     - Username: `testuser1`
     - Email: `test1@example.com`
     - Password: `testpass123`
   
   - User 2:
     - Username: `testuser2`
     - Email: `test2@example.com`
     - Password: `testpass123`

### Test Data

The test suite creates the following test data:

1. Tasks:
   - Name: "Test Task"
   - Description: "Test Description"
   - Task Type: "development"
   - Status: "pending"
   - Created by: testuser1
   - Assigned to: testuser2

2. Task Types:
   - development
   - testing
   - documentation
   - deployment
   - other

3. Task Statuses:
   - pending
   - in_progress
   - completed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 