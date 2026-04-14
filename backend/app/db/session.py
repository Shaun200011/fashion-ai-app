from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings


def _ensure_sqlite_parent_dir() -> None:
    if settings.sqlite_url.startswith("sqlite:///"):
        db_path = Path(settings.sqlite_url.removeprefix("sqlite:///"))
        if db_path.parent != Path("."):
            db_path.parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_parent_dir()
engine = create_engine(settings.sqlite_url, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
