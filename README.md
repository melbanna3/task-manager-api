# Task Manager API
A REST API for managing tasks, built with FastAPI and PostgreSQL.

## Endpoints
- GET /tasks: List all tasks (optional query param: `status`, e.g., `/tasks?status=pending`).
- GET /tasks/{id}: Fetch a single task by ID.
- POST /tasks: Create a task (validates unique ID, non-empty title/description, status as `pending` or `completed`).
- PUT /tasks/{id}: Update a task.
- DELETE /tasks/{id}: Delete a task.

## Setup
1. Install PostgreSQL: `brew install postgresql` (macOS) and start: `brew services start postgresql`.
2. Create database: `createdb task_manager`.
3. Install Python dependencies: `pip install -r requirements.txt`.
4. Run: `uvicorn main:app --reload`.

## Database
- Uses PostgreSQL with SQLAlchemy for persistent storage.
- Table: `tasks` (columns: `id`, `title`, `description`, `status`).

## Testing
- Use curl: `curl http://127.0.0.1:8000/tasks?status=pending`.
- Use Postman: Send requests to `http://127.0.0.1:8000/tasks` with query params or JSON bodies.
- Visit `http://127.0.0.1:8000/docs` for interactive docs.