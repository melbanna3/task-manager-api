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

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
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