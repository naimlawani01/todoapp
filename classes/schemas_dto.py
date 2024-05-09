from pydantic import BaseModel
class Task(BaseModel):
    id: str
    title: str
    description: str
    done: bool

class TaskNoId(BaseModel):
    title: str
    description: str
    done: bool


class User(BaseModel):
    email: str
    password: str  