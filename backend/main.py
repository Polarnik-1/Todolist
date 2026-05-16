from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import engine, Base




from app.service import service
from app.database.database import SessionLocal
from app.schemas import schemas
from config import settings
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc',
    redirect_slashes=True
)
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return service.create_task(db=db, task=task)


@app.get("/tasks/", response_model=List[schemas.Task]) # Обязательно List[...]
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = service.get_tasks(db, skip=skip, limit=limit)
    return tasks

# Маршрут для получения задачи по ID
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    print(f"Запрос на поиск задачи с ID: {task_id}")  # Это появится в консоли Uvicorn

    db_task = service.get_task(db, task_id=task_id)

    if db_task is None:
        print(f"Задача {task_id} не найдена в БД")
        raise HTTPException(status_code=404, detail="Task not found")

    return db_task

# Маршрут для удаления задачи по ID
@app.delete("/tasks/{task_id}/", response_model=schemas.Task)
def delete_task(task_id:int, db: Session = Depends(get_db)):
    db_task = service.delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task






