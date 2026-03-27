from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Task:
    id: int | None
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
