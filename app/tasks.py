class TaskManager:
    def __init__(self):
        self.tasks = {}

    def create_task(self, task_id: str):
        self.tasks[task_id] = "PENDING"

    def update_task(self, task_id: str, status: str):
        self.tasks[task_id] = status

    def get_task_status(self, task_id: str):
        return self.tasks.get(task_id)
