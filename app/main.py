from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from . import models
from .schemas import TaskOut, TaskCreate

from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Task API Root - use /tasks to manage tasks"}

@router.post("/tasks", response_model=TaskOut)
def create_task(task:TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# ✅ GET all tasks
@router.get("/tasks", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# ✅ PUT update task
@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, updated_data: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_data.title
    task.description = updated_data.description
    task.time_to_complete = updated_data.time_to_complete
    db.commit()
    db.refresh(task)
    return task

# ✅ DELETE task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}
