from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from app.database import get_db
from app import crud, schemas, models
from typing import List
from app.auth import get_current_user
from app.schemas import LogOut, LogCreate, LogUpdate, UserRole

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
)

# Получение списка всех записей (доступно администратору и проверяющему)
@router.get("/", response_model=List[LogOut])
async def get_logs(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value == UserRole.digitizer.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    query = select(models.Log)
    if current_user.role.value == UserRole.reviewer.value:
        query = query.filter(models.Log.assigned_to == current_user.id)

    result = await db.execute(query)
    logs = result.scalars().all()
    return logs

# Создание новой записи (доступно администратору и проверяющему)
@router.post("/", response_model=LogOut)
async def create_log(log: LogCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value not in [UserRole.admin.value, UserRole.reviewer.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    new_log = models.Log(
        **log.dict(),
        assigned_to=current_user.id,  # Назначаем текущего пользователя как исполнителя
        created_at=func.now(),
        updated_at=func.now()
    )
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

# Обновление записи (доступно администратору и проверяющему)
@router.put("/{log_id}", response_model=LogOut)
async def update_log(log_id: int, log: LogUpdate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing_log = await crud.get_log_by_id(db, log_id)
    if not existing_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")

    if current_user.role.value == UserRole.digitizer.value or (current_user.role.value == UserRole.reviewer.value and existing_log.assigned_to != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    for key, value in log.dict(exclude_unset=True).items():
        setattr(existing_log, key, value)

    existing_log.updated_at = func.now()  # Обновляем время последнего изменения

    db.add(existing_log)
    await db.commit()
    await db.refresh(existing_log)
    return existing_log

# Удаление записи (доступно только администратору)
@router.delete("/{log_id}", response_model=LogOut)
async def delete_log(log_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value != UserRole.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    existing_log = await crud.get_log_by_id(db, log_id)
    if not existing_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")

    await db.delete(existing_log)
    await db.commit()
    return existing_log
