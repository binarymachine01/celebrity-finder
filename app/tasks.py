from celery import Celery
import time


celery = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")


@celery.task
def process_data_task(data: str):
    time.sleep(5)
    return {"processed_data": data.upper()}
