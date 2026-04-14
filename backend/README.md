# Backend

FastAPI service for upload, classification, metadata storage, and search APIs.

## Current Classification Design

- `classification_provider.py` defines the provider abstraction
- `classification_parser.py` normalizes provider output into the app schema
- The app currently uses a mock provider, but the service boundary now matches a real AI integration flow

## Environment Hooks

- `AI_PROVIDER=auto` uses OpenAI when `OPENAI_API_KEY` is present, otherwise falls back to mock
- `AI_PROVIDER=mock` forces placeholder classification
- `AI_PROVIDER=openai` requires `OPENAI_API_KEY`
