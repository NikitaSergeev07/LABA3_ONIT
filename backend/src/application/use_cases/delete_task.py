from src.domain.repositories.task_repository import TaskRepository


class DeleteTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, task_id: int) -> bool:
        return self.repository.delete(task_id)
