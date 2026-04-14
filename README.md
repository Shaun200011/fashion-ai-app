# Fashion AI App

Fashion AI App is a lightweight inspiration library for fashion designers. It helps users upload field photos, classify garments with multimodal AI, search the library with structured filters, and add human annotations over time.

## Architecture Direction

- `frontend/`: Next.js client for image upload, visual browsing, filtering, and annotation workflows
- `backend/`: FastAPI service for ingestion, AI classification, metadata storage, and search APIs
- `eval/`: Python evaluation scripts, labeled examples, and simple reporting outputs

## Product Scope

The first version is intentionally narrow:

- Single-user local development setup
- Local image storage
- Structured AI metadata with validation
- Full-text search plus dynamic filters
- Manual designer tags and notes

## Implementation Plan

1. Scaffold the repo, backend API, and project documentation
2. Define the data model and classification schema
3. Build upload and local asset storage
4. Add classification orchestration and metadata persistence
5. Build the UI grid, search, and dynamic filters
6. Add annotations, tests, and evaluation

## Why This Stack

- Python aligns with the AI systems focus of the target role
- FastAPI keeps the backend service lightweight and production-flavored
- Next.js provides a clean path for a polished UI
- SQLite keeps local setup simple for a take-home project

## Initial Local Setup

Backend setup will use the existing virtual environment:

```bash
cd /Users/yuxiang/fashion-ai-app/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The frontend will be added next in `frontend/`.

Frontend setup:

```bash
cd /Users/yuxiang/fashion-ai-app/frontend
npm install
npm run dev
```

## Current Backend Endpoints

- `GET /api/health`: simple readiness check
- `POST /api/images/upload`: accepts a multipart image upload, stores the file locally, and creates placeholder AI metadata
- `GET /api/images`: returns uploaded images with attached AI metadata and supports query/filter parameters
- `GET /api/filters`: returns dynamic filter groups aggregated from stored AI metadata
- `POST /api/images/{image_id}/classify`: reruns placeholder classification for a stored image
- `POST /api/images/{image_id}/annotations`: creates a designer note or tag linked to an image

## Current Frontend Status

- Next.js app skeleton with App Router structure
- Editorial landing page tailored to the fashion inspiration use case
- Shared TypeScript types and backend API client helpers
- Homepage library reads live image data and supports basic browser-based upload
- Homepage supports live text search and dynamic filter interaction
- Homepage supports lightweight designer note annotations

## Current Classification Status

- The backend now routes classification through a provider abstraction instead of embedding placeholder logic directly in route handlers
- Provider output is normalized through a dedicated parser before persistence
- `AI_PROVIDER=auto` will attempt a real OpenAI-backed provider when `OPENAI_API_KEY` is configured, then fall back to the mock provider when local setup is incomplete

## Environment Variables

For local development, the app works without any API keys.

If you want to enable the real provider path later, set:

```bash
export AI_PROVIDER=auto
export OPENAI_API_KEY=your_api_key_here
```
