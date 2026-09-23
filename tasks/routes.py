from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.core.database import get_db
from tasks import models, schemas
from tasks.models import TaskModel
from tasks.schemas import TaskResponse


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/tasks", response_model=list[TaskResponse])
async def retrieve_tasks_list(
    completed: bool = Query(None, description="filter tasks based on being completed or not"),
    limit: int = Query(10, gt=0, le=50, description="limiting the number of items to retrieve"),
    offset: int = Query(0, ge=0, description="how many items to skip"),
    db: Session = Depends(get_db),
):
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter_by(is_completed=completed)

    return query.offset(offset).limit(limit).all()


@router.get("/{id}", response_model=schemas.TaskResponse)
def retrieve_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskModel).filter(models.TaskModel.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.TaskModel(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{id}", response_model=schemas.TaskResponse)
def update_task(id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.TaskModel).filter(models.TaskModel.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskModel).filter(models.TaskModel.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()