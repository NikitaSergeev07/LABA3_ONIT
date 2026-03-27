from sqlalchemy.orm import Session

from src.domain.entities.task import Task
from src.domain.repositories.task_repository import TaskRepository
from src.infrastructure.orm.models import TaskModel


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_entity(model: TaskModel) -> Task:
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            is_done=model.is_done,
            created_at=model.created_at,
        )

    def list(self) -> list[Task]:
        items = self.db.query(TaskModel).order_by(TaskModel.created_at.desc()).all()
        return [self._to_entity(item) for item in items]

    def get_by_id(self, task_id: int) -> Task | None:
        item = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if item is None:
            return None
        return self._to_entity(item)

    def create(self, title: str, description: str | None) -> Task:
        item = TaskModel(title=title, description=description)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return self._to_entity(item)

    def update(
        self,
        task_id: int,
        title: str,
        description: str | None,
        is_done: bool,
    ) -> Task | None:
        item = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if item is None:
            return None

        item.title = title
        item.description = description
        item.is_done = is_done

        self.db.commit()
        self.db.refresh(item)
        return self._to_entity(item)

    def delete(self, task_id: int) -> bool:
        item = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if item is None:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
