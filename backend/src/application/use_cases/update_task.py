from src.application.dtos.task_dto import TaskUpdateDTO
from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository


class UpdateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, task_id: int, data: TaskUpdateDTO) -> Task | None:
        current = self.repository.get_by_id(task_id)
        if current is None:
            return None

        title = data.title.strip() if data.title is not None else current.title
        if not title:
            raise ValueError("Название задачи не может быть пустым")

        description = (
            data.description.strip() if data.description is not None else current.description
        )
        if description == "":
            description = None

        is_done = data.is_done if data.is_done is not None else current.is_done

        return self.repository.update(
            task_id=task_id,
            title=title,
            description=description,
            is_done=is_done,
        )
