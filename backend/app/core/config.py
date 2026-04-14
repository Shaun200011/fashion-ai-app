import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _load_dotenv() -> dict[str, str]:
    env_path = PROJECT_ROOT / ".env"
    values: dict[str, str] = {}

    if not env_path.exists():
        return values

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'").strip('"')

    return values


DOTENV_VALUES = _load_dotenv()


def _env(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, DOTENV_VALUES.get(key, default))


class Settings(BaseModel):
    app_name: str = _env("APP_NAME", "Fashion AI App API") or "Fashion AI App API"
    app_version: str = _env("APP_VERSION", "0.1.0") or "0.1.0"
    api_prefix: str = _env("API_PREFIX", "/api") or "/api"
    local_image_dir: str = _env("LOCAL_IMAGE_DIR", "data/images") or "data/images"
    sqlite_url: str = _env("SQLITE_URL", "sqlite:///data/fashion_ai_app.db") or "sqlite:///data/fashion_ai_app.db"
    cors_origins: list[str] = [
        origin.strip()
        for origin in (_env("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000") or "").split(",")
        if origin.strip()
    ]
    ai_provider: str = _env("AI_PROVIDER", "auto") or "auto"
    openai_api_key: Optional[str] = _env("OPENAI_API_KEY")
    openai_base_url: str = (
        _env("OPENAI_BASE_URL", "https://api.openai.com/v1/responses")
        or "https://api.openai.com/v1/responses"
    )
    openai_model: str = _env("OPENAI_MODEL", "gpt-4.1-mini") or "gpt-4.1-mini"
    openai_timeout_seconds: int = int(_env("OPENAI_TIMEOUT_SECONDS", "45") or "45")
    openai_image_detail: str = _env("OPENAI_IMAGE_DETAIL", "low") or "low"


settings = Settings()
