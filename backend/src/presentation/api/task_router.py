from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.application.dtos.task_dto import TaskCreateDTO, TaskUpdateDTO
from src.application.use_cases.create_task import CreateTaskUseCase
from src.application.use_cases.delete_task import DeleteTaskUseCase
from src.application.use_cases.get_task import GetTaskUseCase
from src.application.use_cases.list_tasks import ListTasksUseCase
from src.application.use_cases.update_task import UpdateTaskUseCase
from src.domain.entities.task import Task
from src.presentation.dependencies import (
    get_create_task_use_case,
    get_delete_task_use_case,
    get_get_task_use_case,
    get_list_tasks_use_case,
    get_update_task_use_case,
)
from src.presentation.schemas.task_schema import (
    TaskCreateRequest,
    TaskResponse,
    TaskUpdateRequest,
)


router = APIRouter(prefix="/tasks", tags=["tasks"])


def to_response(task: Task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        created_at=task.created_at,
    )


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    use_case: ListTasksUseCase = Depends(get_list_tasks_use_case),
) -> list[TaskResponse]:
    tasks = use_case.execute()
    return [to_response(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    use_case: GetTaskUseCase = Depends(get_get_task_use_case),
) -> TaskResponse:
    task = use_case.execute(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return to_response(task)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateRequest,
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case),
) -> TaskResponse:
    try:
        task = use_case.execute(
            TaskCreateDTO(
                title=payload.title,
                description=payload.description,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdateRequest,
    use_case: UpdateTaskUseCase = Depends(get_update_task_use_case),
) -> TaskResponse:
    try:
        task = use_case.execute(
            task_id,
            TaskUpdateDTO(
                title=payload.title,
                description=payload.description,
                is_done=payload.is_done,
            ),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return to_response(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    use_case: DeleteTaskUseCase = Depends(get_delete_task_use_case),
) -> Response:
    deleted = use_case.execute(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
