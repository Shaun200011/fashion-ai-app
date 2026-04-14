from sqlmodel import Session, SQLModel, create_engine

sqlite_url = "sqlite:///fashion_ai_app.db"
engine = create_engine(sqlite_url, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

