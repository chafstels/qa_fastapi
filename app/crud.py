from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.auth import get_password_hash


# Создание пользователя
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    password_hash = get_password_hash(user.password)

    # Добавляем поле email при создании пользователя
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        role=user.role
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# Получение пользователя по имени
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()


# Получение пользователя по ID
async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

# Получение пользователя по email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()
