from sqlalchemy import create_engine, pool
from alembic import context
from app.database import Base  # Импортируем Base из вашего проекта
from app import models  # Явно импортируем модели, чтобы Alembic их увидел

# Эта строка конфигурации позволяет Alembic получить URL базы данных из alembic.ini
config = context.config

# Создаем синхронную версию URL базы данных для миграций
SYNC_DATABASE_URL = config.get_main_option("sqlalchemy.url")

# Метаданные моделей из базы данных
target_metadata = Base.metadata

# Проверка наличия таблиц в метаданных
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('alembic.runtime.migration')
logger.info(f"Metatada tables: {Base.metadata.tables.keys()}")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = SYNC_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        SYNC_DATABASE_URL, poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
