from app.core.config import settings
from app.services.classification_provider import (
    MockClassificationProvider,
    OpenAIClassificationProvider,
    get_classification_provider,
)


def test_get_classification_provider_uses_mock_without_api_key() -> None:
    original_provider = settings.ai_provider
    original_api_key = settings.openai_api_key
    settings.ai_provider = "auto"
    settings.openai_api_key = None

    try:
        provider = get_classification_provider()
        assert isinstance(provider, MockClassificationProvider)
    finally:
        settings.ai_provider = original_provider
        settings.openai_api_key = original_api_key


def test_get_classification_provider_uses_openai_when_key_present() -> None:
    original_provider = settings.ai_provider
    original_api_key = settings.openai_api_key
    settings.ai_provider = "auto"
    settings.openai_api_key = "test-key"

    try:
        provider = get_classification_provider()
        assert isinstance(provider, OpenAIClassificationProvider)
    finally:
        settings.ai_provider = original_provider
        settings.openai_api_key = original_api_key
