from src.application.dtos.task_dto import TaskCreateDTO
from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository


class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, data: TaskCreateDTO) -> Task:
        title = data.title.strip()
        if not title:
            raise ValueError("Название задачи не может быть пустым")

        description = data.description.strip() if data.description else None
        if description == "":
            description = None

        return self.repository.create(title=title, description=description)
