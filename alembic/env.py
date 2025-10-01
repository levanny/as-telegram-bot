import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from database.models import Base, DATABASE_URL

# Alembic Config object, provides access to values in .ini file
config = context.config

# Setup Python logging from config file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use your models' metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()



async def run_migrations_online():
    """Run migrations in 'online' (async) mode."""
    connectable = create_async_engine(DATABASE_URL, echo=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
