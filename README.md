# Task Manager API
A REST API for managing tasks, built with FastAPI and PostgreSQL.

## Endpoints
- POST /users: Register a user.
- POST /token: Login to get a JWT.
- GET /tasks: List tasks (optional query param: `status`, e.g., `/tasks?status=pending`).
- GET /tasks/{id}: Fetch a task by ID.
- POST /tasks: Create a task.
- PUT /tasks/{id}: Update a task.
- DELETE /tasks/{id}: Delete a task.

## Setup
1. Install PostgreSQL: `brew install postgresql` (macOS) and start: `brew services start postgresql`.
2. Create database: `createdb task_manager`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run: `uvicorn main:app --reload`.

## Authentication
- Uses JWT for securing endpoints.
- Register via `POST /users`, login via `POST /token`, then include `Authorization: Bearer <token>` in headers.

## Database
- PostgreSQL with SQLAlchemy.
- Tables: `users` (id, username, hashed_password), `tasks` (id, title, description, status, user_id).

## Testing
- Use curl: `curl -X POST "http://127.0.0.1:8000/token" -d "username=mahmoud&password=securepassword"`.
- Use Postman: Send requests with JSON bodies and Bearer tokens.
- Visit `http://127.0.0.1:8000/docs` for interactive docs.