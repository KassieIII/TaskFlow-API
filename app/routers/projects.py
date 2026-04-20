from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project)
        .where(Project.owner_id == current_user.id, Project.is_archived == False)
        .order_by(Project.updated_at.desc())
    )
    projects = result.scalars().all()

    response = []
    for project in projects:
        task_count_result = await db.execute(
            select(func.count(Task.id)).where(Task.project_id == project.id)
        )
        task_count = task_count_result.scalar() or 0
        proj_dict = ProjectResponse.model_validate(project)
        proj_dict.task_count = task_count
        response.append(proj_dict)

    return response


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = Project(
        name=data.name,
        description=data.description,
        owner_id=current_user.id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = await _get_user_project(db, project_id, current_user.id)
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = await _get_user_project(db, project_id, current_user.id)

    if data.name is not None:
        project.name = data.name
    if data.description is not None:
        project.description = data.description

    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = await _get_user_project(db, project_id, current_user.id)
    project.is_archived = True
    await db.commit()


async def _get_user_project(db: AsyncSession, project_id: int, user_id: int) -> Project:
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == user_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project
