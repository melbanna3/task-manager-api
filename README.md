# Task Manager API
A REST API for managing tasks, built with FastAPI.

## Endpoints
- GET /tasks: List all tasks.
- POST /tasks: Create a task.
- PUT /tasks/{id}: Update a task.
- DELETE /tasks/{id}: Delete a task.

## Setup
1. Install dependencies: `pip install fastapi uvicorn`
2. Run: `uvicorn main:app --reload`

## Testing
- Use curl: `curl http://127.0.0.1:8000/tasks`
- Use Postman: Send requests to `http://127.0.0.1:8000/tasks` with JSON bodies.
- Visit `http://127.0.0.1:8000/docs` for interactive docs.