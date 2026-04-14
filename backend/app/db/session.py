from pathlib import Path

from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings


def _ensure_sqlite_parent_dir() -> None:
    if settings.sqlite_url.startswith("sqlite:///"):
        db_path = Path(settings.sqlite_url.removeprefix("sqlite:///"))
        if db_path.parent != Path("."):
            db_path.parent.mkdir(parents=True, exist_ok=True)


def get_engine():
    _ensure_sqlite_parent_dir()
    return create_engine(settings.sqlite_url, echo=False)


def init_db() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    _run_sqlite_migrations(engine)


def get_session():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    _run_sqlite_migrations(engine)
    with Session(engine) as session:
        yield session


def _run_sqlite_migrations(engine) -> None:
    if not settings.sqlite_url.startswith("sqlite:///"):
        return

    with engine.begin() as connection:
        columns = connection.execute(text("PRAGMA table_info(annotation)")).fetchall()
        column_names = {column[1] for column in columns}

        if columns and "author" not in column_names:
            connection.execute(text("ALTER TABLE annotation ADD COLUMN author VARCHAR"))
