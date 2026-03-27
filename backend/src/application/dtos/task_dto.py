from dataclasses import dataclass


@dataclass(slots=True)
class TaskCreateDTO:
    title: str
    description: str | None = None


@dataclass(slots=True)
class TaskUpdateDTO:
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None
