import uuid
from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis
from app.rekognition import analyze_image_async
from app.auth import authenticate_user
from app.tasks import TaskManager
from config import RATE_LIMIT_REQUESTS, RATE_LIMIT_PERIOD

app = FastAPI()
security = HTTPBasic()
task_manager = TaskManager()


@app.on_event("startup")
async def startup():
    redis = Redis(host="localhost", port=6379, decode_responses=True)
    await FastAPILimiter.init(redis)


@app.post("/process-image/", dependencies=[Depends(RateLimiter(times=RATE_LIMIT_REQUESTS,
                                                               seconds=RATE_LIMIT_PERIOD))])
async def process_image(
    file: UploadFile, background_tasks: BackgroundTasks, credentials: HTTPBasicCredentials = Depends(security)
):

    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Unauthorized")


    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are supported.")


    file_content = await file.read()


    task_id = str(uuid.uuid4())
    task_manager.create_task(task_id)


    background_tasks.add_task(analyze_image_async, task_id, file_content, task_manager)
    return {"task_id": task_id, "message": "Processing started asynchronously!"}


@app.get("/task-status/{task_id}")
async def task_status(task_id: str, credentials: HTTPBasicCredentials = Depends(security)):

    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Unauthorized")


    status = task_manager.get_task_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task ID not found")

    return {"task_id": task_id, "status": status}
