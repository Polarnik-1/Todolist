
from sqlalchemy.orm import Session
from ..model import model
from ..schemas import schemas


def get_task(db, task_id: int):
    # Используем .filter() по полю id
    return db.query(model.Task).filter(model.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = model.Task(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task =get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()

        return db_task
    return None


