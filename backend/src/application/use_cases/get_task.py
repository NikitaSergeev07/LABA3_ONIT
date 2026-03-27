from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository


class GetTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)
