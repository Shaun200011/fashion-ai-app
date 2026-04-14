# Backend

FastAPI service for upload, classification, metadata storage, and search APIs.

## Current Classification Design

- `classification_provider.py` defines the provider abstraction
- `classification_parser.py` normalizes provider output into the app schema
- The app currently uses a mock provider, but the service boundary now matches a real AI integration flow
