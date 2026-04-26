from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskAssign, TaskResponse
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
async def list_tasks(
    project_id: int,
    status_filter: TaskStatus | None = Query(None, alias="status"),
    priority: TaskPriority | None = None,
    assignee_id: int | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _verify_project_access(db, project_id, current_user.id)

    query = select(Task).where(Task.project_id == project_id)

    if status_filter:
        query = query.where(Task.status == status_filter)
    if priority:
        query = query.where(Task.priority == priority)
    if assignee_id:
        query = query.where(Task.assignee_id == assignee_id)
    if search:
        query = query.where(Task.title.ilike(f"%{search}%"))

    offset = (page - 1) * per_page
    query = query.order_by(Task.created_at.desc()).offset(offset).limit(per_page)

    result = await db.execute(query)
    return result.scalars().all()


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: int,
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _verify_project_access(db, project_id, current_user.id)

    task = Task(
        title=data.title,
        description=data.description,
        priority=data.priority,
        project_id=project_id,
        assignee_id=data.assignee_id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await _get_task(db, task_id, current_user.id)
    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await _get_task(db, task_id, current_user.id)

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.priority is not None:
        task.priority = data.priority

    await db.commit()
    await db.refresh(task)
    return task


@router.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def change_task_status(
    task_id: int,
    data: TaskStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await _get_task(db, task_id, current_user.id)
    task.status = data.status
    await db.commit()
    await db.refresh(task)
    return task


@router.patch("/tasks/{task_id}/assign", response_model=TaskResponse)
async def assign_task(
    task_id: int,
    data: TaskAssign,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await _get_task(db, task_id, current_user.id)
    task.assignee_id = data.assignee_id
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await _get_task(db, task_id, current_user.id)
    await db.delete(task)
    await db.commit()


async def _verify_project_access(db: AsyncSession, project_id: int, user_id: int):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == user_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


async def _get_task(db: AsyncSession, task_id: int, user_id: int) -> Task:
    result = await db.execute(
        select(Task).join(Project).where(Task.id == task_id, Project.owner_id == user_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task
