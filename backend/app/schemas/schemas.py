from pydantic import BaseModel



class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool

class TaskCreate(TaskBase):
    pass


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool

    class Config:
        from_attributes = True











