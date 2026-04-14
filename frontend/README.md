# Frontend

Next.js app for the design-facing workflow.

## Planned Responsibilities

- Upload garment images
- Display the inspiration library in an editorial grid
- Surface AI metadata and designer notes separately
- Support search and dynamic filtering against the backend API

## Current Status

- The homepage loads live data from `GET /api/images` when the backend is running
- The homepage can upload a new image to `POST /api/images/upload`
- The homepage supports live search and dynamic filter pills sourced from `GET /api/filters`
- Each image card can submit and display designer notes through the annotation API
- If the backend is unavailable, the UI falls back to editorial sample content so design work can continue

## Local Setup

```bash
cd /Users/yuxiang/fashion-ai-app/frontend
npm install
npm run dev
```

## End-to-End Test

The Playwright happy-path test expects the backend to be running on `http://127.0.0.1:8000`.

```bash
cd /Users/yuxiang/fashion-ai-app/frontend
npx playwright install
npm run test:e2e
```
