from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Fashion AI App API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    local_image_dir: str = "data/images"
    sqlite_url: str = "sqlite:///data/fashion_ai_app.db"


settings = Settings()
