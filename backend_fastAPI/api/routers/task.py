from fastapi import status, APIRouter, Depends

from backend_fastAPI.api.dependencies import get_task_service
from backend_fastAPI.schemas.tasks import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from backend_fastAPI.services.task import TaskService

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('', status_code=status.HTTP_200_OK)
def get_tasks(task_service: TaskService = Depends(get_task_service)) ->list[TaskSchema]:
    return task_service.list_tasks()


@router.post('', status_code=status.HTTP_201_CREATED)
def create_task(payload:TaskCreateSchema, task_service: TaskService = Depends(get_task_service)):
    return task_service.create_task(task_create=payload)

@router.patch('/{task_id}', status_code=status.HTTP_200_OK)
def update_task(task_id, payload:TaskUpdateSchema, task_service: TaskService = Depends(get_task_service)):
    return task_service.update_task(task_id=task_id, task_update=payload)

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, task_service: TaskService = Depends(get_task_service)):
    return task_service.delete_task(task_id=task_id)


