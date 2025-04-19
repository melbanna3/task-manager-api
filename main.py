from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, field_validator
from typing import List
from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "postgresql://localhost/task_manager"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Task model
class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    # Alternatively, you can use ENUM for status in the database
        # from sqlalchemy.dialects.postgresql import ENUM
        # status = Column(ENUM('pending', 'completed', name='task_status'), nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus

    @field_validator('title', 'description')
    def check_not_empty(cls, value):
        if not value.strip():
            raise ValueError('Field cannot be empty')
        return value

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Manager API!"}

@app.get("/tasks", response_model=List[Task])
def get_tasks(status: str = None, db: SessionLocal = Depends(get_db)):
    query = db.query(TaskDB)
    if status:
        query = query.filter(TaskDB.status == status)
    return query.all()

@app.post("/tasks", response_model=Task)
def create_task(task: Task, db: SessionLocal = Depends(get_db)):
    for existing_task in db.query(TaskDB).all():
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Task ID already exists")
    db_task = TaskDB(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task, db: SessionLocal = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updated_task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: SessionLocal = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: SessionLocal = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task