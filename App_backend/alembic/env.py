from logging.config import fileConfig
import os

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Import your SQLAlchemy Base
from database import Base

# Import all models so Alembic can detect them
import models

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# -------------------------------------------------
# Alembic Config
# -------------------------------------------------

config = context.config

config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------
# Metadata
# -------------------------------------------------

target_metadata = Base.metadata


# -------------------------------------------------
# Offline Migration
# -------------------------------------------------

def run_migrations_offline():

    context.configure(

        url=DATABASE_URL,

        target_metadata=target_metadata,

        literal_binds=True,

        dialect_opts={"paramstyle": "named"},

        compare_type=True,

    )

    with context.begin_transaction():

        context.run_migrations()


# -------------------------------------------------
# Online Migration
# -------------------------------------------------

def run_migrations_online():

    connectable = create_engine(

        DATABASE_URL,

        poolclass=pool.NullPool

    )

    with connectable.connect() as connection:

        context.configure(

            connection=connection,

            target_metadata=target_metadata,

            compare_type=True

        )

        with context.begin_transaction():

            context.run_migrations()


# -------------------------------------------------

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()