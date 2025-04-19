from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Task model
class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str

# In-memory storage
tasks = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager API!"}

@app.get("/tasks", response_model=List[Task])
def get_tasks(status: str = None):
    if status:
        return [task for task in tasks if task.status == status]
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Task ID already exists")
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updateed_task: Task):
    for index, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            tasks[index] = updateed_task
            return updateed_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")