from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.use_cases.create_task import CreateTaskUseCase
from src.application.use_cases.delete_task import DeleteTaskUseCase
from src.application.use_cases.get_task import GetTaskUseCase
from src.application.use_cases.list_tasks import ListTasksUseCase
from src.application.use_cases.update_task import UpdateTaskUseCase
from src.core.database import get_db
from src.domain.repositories.task_repository import TaskRepository
from src.infrastructure.repositories.sqlalchemy_task_repository import SQLAlchemyTaskRepository


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return SQLAlchemyTaskRepository(db)


def get_create_task_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> CreateTaskUseCase:
    return CreateTaskUseCase(repository)


def get_list_tasks_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> ListTasksUseCase:
    return ListTasksUseCase(repository)


def get_get_task_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> GetTaskUseCase:
    return GetTaskUseCase(repository)


def get_update_task_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> UpdateTaskUseCase:
    return UpdateTaskUseCase(repository)


def get_delete_task_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> DeleteTaskUseCase:
    return DeleteTaskUseCase(repository)
