import asyncio
from sqlalchemy import text
from app.database import get_db

async def check_db_connection():
    # Создание сессии через асинхронный генератор
    async for session in get_db():
        try:
            # Выполнение тестового запроса
            await session.execute(text("SELECT 1"))
            print("Соединение с базой данных успешно установлено.")
        except Exception as e:
            print("Ошибка подключения к базе данных:", e)

if __name__ == "__main__":
    asyncio.run(check_db_connection())
