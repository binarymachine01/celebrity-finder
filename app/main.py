from fastapi import FastAPI, Depends
from celery import Celery
from app.auth import authenticate
from pydantic import BaseModel
import os

# Initialize FastAPI
app = FastAPI()

# Celery setup
celery = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/0"),
)


class DataRequest(BaseModel):
    data: str

@app.post("/submit")
async def submit_data(request: DataRequest, username: str = Depends(authenticate)):
    task = celery.send_task("app.tasks.process_data", args=[request.data])
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def check_status(task_id: str, username: str = Depends(authenticate)):
    task = celery.AsyncResult(task_id)
    if task.state == "PENDING":
        return {"state": "PENDING", "result": None}
    elif task.state == "FAILURE":
        return {"state": "FAILURE", "error": str(task.info)}
    return {"state": task.state, "result": task.result}
