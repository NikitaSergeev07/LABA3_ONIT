from abc import ABC, abstractmethod

from src.domain.entities.task import Task


class TaskRepository(ABC):
    @abstractmethod
    def list(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, title: str, description: str | None) -> Task:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        task_id: int,
        title: str,
        description: str | None,
        is_done: bool,
    ) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        raise NotImplementedError
