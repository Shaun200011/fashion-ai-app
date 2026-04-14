from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.config import settings
from app.db.session import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="Backend service for garment classification and inspiration search.",
        version=settings.app_version,
    )

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_app()
