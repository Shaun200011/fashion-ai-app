# Frontend

Next.js app for the design-facing workflow.

## Planned Responsibilities

- Upload garment images
- Display the inspiration library in an editorial grid
- Surface AI metadata and designer notes separately
- Support search and dynamic filtering against the backend API

## Current Status

- The homepage loads live data from `GET /api/images` when the backend is running
- If the backend is unavailable, the UI falls back to editorial sample content so design work can continue

## Local Setup

```bash
cd /Users/yuxiang/fashion-ai-app/frontend
npm install
npm run dev
```
