from typing import List
from fastapi import APIRouter, Depends, HTTPException
from classes.schemas_dto import Task, TaskNoId
from database.firebase import db
from routers.router_auth import get_current_user
import uuid



router = APIRouter()

@router.get("/tasks/", response_model=List[Task])
async def get_all_tasks():
    try:
        tasks = []
        task_docs = db.collection('tasks').stream()
        for doc in task_docs:
            task_data = doc.to_dict()
            tasks.append(Task(**task_data))
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks/", response_model=Task)
async def create_task(task: TaskNoId, userData: int = Depends(get_current_user)):
    try:
        task_id = str(uuid.uuid4())
        db.child('tasks').child(task_id).set({**task.dict(), "id": task_id})
        return Task(**{"id": task_id, **task.dict()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: str):
    try:
        task = db.child('tasks').child(task_id).get().val()
        if task is not None:
            return task
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskNoId, userData: int = Depends(get_current_user)):

    task_db = db.child('tasks').child(task_id).get().val()
    if task_db is not None:
        updatedTask = Task(id=task_id, **task.model_dump())
        return db.child('tasks').child(task_id).update(updatedTask.model_dump())
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, userData: int = Depends(get_current_user)):
    try:
        task_db = db.child('tasks').child(task_id).get().val()
        if task_db is not None:
            return db.child('tasks').child(task_id).remove()
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
