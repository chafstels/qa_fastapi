from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app import crud, schemas, models
from typing import List
from app.auth import get_current_user
from app.schemas import UserOut, UserRole, UserUpdateRole

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Получение списка всех пользователей (доступно только администраторам)
@router.get("/", response_model=List[UserOut])
async def get_users(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.value != UserRole.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users

# Обновление роли пользователя (доступно только администраторам)
@router.put("/{user_id}", response_model=UserOut)
async def update_user_role(user_id: int, user_update: UserUpdateRole, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.value != UserRole.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Получаем пользователя для обновления
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Обновляем роль пользователя
    user.role = user_update.role
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Удаление пользователя (доступно только администраторам)
@router.delete("/{user_id}", response_model=UserOut)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Проверяем, является ли текущий пользователь администратором
    if current_user.role.value != UserRole.admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Получаем пользователя для удаления
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await db.delete(user)
    await db.commit()
    return user
