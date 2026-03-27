from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository


class ListTasksUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self) -> list[Task]:
        return self.repository.list()
