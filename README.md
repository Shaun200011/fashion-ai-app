# Fashion AI App

Fashion AI App is a lightweight web application for organizing fashion inspiration imagery. Designers can upload field photos, generate structured garment metadata, search the library with dynamic filters, and add their own notes over time.

This project is intentionally scoped as a one-day proof of concept. The focus is on a strong end-to-end workflow, clean service boundaries, a realistic evaluation scaffold, and honest trade-offs.

## Results Snapshot

The project includes three levels of real-model evaluation using `gpt-4.1-mini`.

| Run | Sample size | garment_type (strict / semantic) | style | occasion (strict / semantic) | season (strict / semantic) | base_colour |
| --- | --- | --- | --- | --- | --- | --- |
| Real-model sanity check | 10 | `90% / 100%` | `100%` | `70% / 70%` | `30% / 60%` | `80%` |
| Real-model subset | 50 | `42% / 56%` | `70.59%` | `66% / 80%` | `50% / 58%` | `82%` |
| Real-model full benchmark | 100 | `43% / 52%` | `78.12%` | `56% / 74%` | `48% / 54%` | `87%` |

The biggest lesson from this progression is that once the real model is active, many of the remaining errors are no longer pure vision failures. They are taxonomy and evaluation problems: `Top` vs `Tops`, `sports bra` vs `Bra`, or `spring/summer` vs a single season label.

## Demo Scope

- Upload garment or street-fashion images from the browser
- Store images locally and persist metadata in SQLite
- Generate structured AI metadata through a provider-based classification pipeline
- Browse the library in a visual grid
- Search across filenames and AI-generated metadata
- Filter by dynamic metadata values aggregated from stored data
- Add designer notes that remain distinct from AI-generated content

## Architecture

```mermaid
flowchart LR
    A["Designer uploads image in Next.js UI"] --> B["FastAPI upload endpoint"]
    B --> C["Local file storage"]
    B --> D["Classification provider"]
    D --> E["Parser / normalizer"]
    E --> F["SQLite metadata tables"]
    F --> G["Image list + filters APIs"]
    G --> H["Library grid, search, filters, designer notes"]
    F --> I["Evaluation script and summary"]
```

### Frontend

- `frontend/`
- Built with Next.js App Router and TypeScript
- Provides the upload flow, editorial-style library UI, live search, dynamic filters, and note entry

### Backend

- `backend/`
- Built with FastAPI, SQLModel, and SQLite
- Handles upload, storage, classification orchestration, filter aggregation, annotations, and evaluation-friendly APIs

### Evaluation

- `eval/`
- Contains dataset placeholders, label manifests, evaluation scripts, and generated summaries
- Now populated with a 100-image evaluation sample drawn from the local fashion dataset

## Repository Structure

```text
backend/   FastAPI API, storage, schemas, services, and tests
frontend/  Next.js UI
eval/      evaluation scripts, labels, and summary output
README.md
```

## Deliverables Checklist

| Area | Status | Notes |
| --- | --- | --- |
| Implementation | Done | Full-stack local app with upload, classification, library browsing, search, filters, and annotations |
| Model Evaluation | Done | Includes 10-image, 50-image, and 100-image real-model benchmarks with strict and semantic scoring |
| Testing | Done | Unit tests, API tests, and a Playwright happy-path test are included |
| Repository Structure | Done | `backend/`, `frontend/`, `eval/`, and root documentation are in place |
| README / Communication | Done | Setup, architecture, trade-offs, evaluation, and limitations are documented |

## Key Technical Decisions

### Python-first backend

The role this project targets emphasizes AI systems and backend engineering, so the application logic is centered in Python. FastAPI was chosen to keep the service lightweight while still looking like a production-style API surface.

### Provider-based classification pipeline

Classification is intentionally split into:

- a provider layer
- a parser/normalizer layer
- a persistence layer

The classification system is split into a provider layer, parser/normalizer layer, and persistence layer so the model can be swapped without changing the rest of the app. In practice, this made it possible to start with a local placeholder provider, then connect the real multimodal path and run the same benchmark pipeline against `gpt-4.1-mini`.

### Dynamic filters from stored metadata

Filter values are not hardcoded in the frontend. The backend aggregates current metadata values from the database and exposes them through `GET /api/filters`, which means available filter pills change as the image library changes.

### Real image thumbnails in the library

Uploaded images are served back through the backend and rendered directly in the library cards. This makes the app feel closer to a real inspiration board and keeps the metadata grounded in the source image.

### AI metadata and human notes are separate

AI-generated metadata is stored and displayed separately from designer annotations. This is important because several target attributes are subjective, and the product should support human correction rather than present AI output as ground truth.

## Proof-of-Concept Trade-Offs

| Decision | Why I chose it | Trade-off |
| --- | --- | --- |
| SQLite over Postgres | Fast local setup and low operational overhead for a take-home | Not designed for multi-user or production-scale workloads |
| Real provider behind environment configuration | Keeps the demo flexible for both local and deployed runs | Public demo environments still need careful API-key handling and cost controls |
| Provider abstraction before real model integration | Keeps the classification pipeline replaceable and testable | Slightly more structure up front than a hardcoded demo call |
| Data-driven filter values with schema-driven filter groups | Meets the prompt requirement without overengineering | Filter dimensions are predefined rather than fully discovered from arbitrary columns |
| Lexical search over embeddings | Faster to implement and easier to explain in a one-day scope | Semantic retrieval quality is limited |
| Source-metadata-based evaluation labels | Makes a 100-image benchmark feasible within time constraints | Some fields are mapped proxies rather than native labels |

## Current API Surface

- `GET /api/health`
- `POST /api/images/upload`
- `GET /api/images`
- `GET /api/filters`
- `POST /api/images/{image_id}/classify`
- `POST /api/images/{image_id}/annotations`

## Local Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

Optional environment setup:

```bash
cp .env.example .env
```

To try the real multimodal path, update `.env` with your API key and keep:

```bash
AI_PROVIDER=auto
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
OPENAI_IMAGE_DETAIL=low
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Run end-to-end coverage:

```bash
cd frontend
npx playwright install
npm run test:e2e
```

Open:

- frontend: `http://localhost:3000`
- backend docs: `http://127.0.0.1:8000/docs`

## Deployment Notes

The application is deployable as two services:

- a Next.js frontend
- a FastAPI backend

For this take-home, the default setup is intentionally local-first:

- SQLite is used for speed and simplicity
- uploaded images are stored on the local filesystem

That means the current code can be deployed for a demo environment, but a production-style deployment should make two changes first:

- replace SQLite with a managed database such as Postgres
- replace local image storage with object storage such as S3 or Cloudinary

The frontend is a straightforward fit for platforms like Vercel. The backend is a straightforward fit for container-friendly platforms such as Render, Fly.io, or Railway.

A starter [render.yaml](render.yaml) is included for a two-service Render deployment, and the frontend now includes an environment template for `NEXT_PUBLIC_API_BASE_URL`.

Minimum deployment environment variables:

- Backend:
  - `AI_PROVIDER`
  - `OPENAI_API_KEY` if real-model inference is enabled
  - `OPENAI_MODEL`
  - `OPENAI_IMAGE_DETAIL`
- Frontend:
  - `NEXT_PUBLIC_API_BASE_URL`

For a public demo, I would still recommend switching:

- `SQLite` -> managed Postgres
- local image files -> object storage

### Quick Deploy Path

If I were shipping this take-home as a lightweight public demo, I would use:

1. `Render` for the FastAPI backend using the included `render.yaml`
2. `Vercel` or `Render` for the Next.js frontend
3. `NEXT_PUBLIC_API_BASE_URL` pointed at the deployed backend `/api`
4. `AI_PROVIDER=auto` with `OPENAI_API_KEY` configured for real inference

That setup would make the project accessible without materially changing the code structure already present in the repository.

## Evaluation Workflow

The evaluation scaffold is implemented and currently runs against a 100-image sample drawn from the local fashion dataset.

Current workflow:

1. Sample images into `eval/dataset/`
2. Review `eval/labels/candidate_labels.json`
3. Run the evaluation script
4. Use the generated `eval/summary.md` in the final write-up

Example:

```bash
cd backend
PYTHONPATH=.:.. python ../eval/run_eval.py
```

The scaffold currently reports per-attribute accuracy for:

- `garment_type`
- `style`
- `occasion`
- `season`
- `base_colour`

These fields were chosen to match the available source metadata in the selected fashion dataset. The original take-home prompt mentions fields such as `material`, but this dataset does not provide reliable material labels, so `base_colour` is used instead as a directly supported visual attribute.

### Full Real-Model Benchmark

The current 100-image benchmark was run against the real multimodal provider using `gpt-4.1-mini`.

- Strict normalized:
  - `garment_type`: `43%`
  - `style`: `78.12%`
  - `occasion`: `56%`
  - `season`: `48%`
  - `base_colour`: `87%`
- Semantic relaxed:
  - `garment_type`: `52%`
  - `style`: `78.12%`
  - `occasion`: `74%`
  - `season`: `54%`
  - `base_colour`: `87%`

### Real-Model Sanity Check

After the end-to-end workflow was stable, I wired the real multimodal provider path and first ran a smaller 10-image sanity check using `gpt-4.1-mini`.

This surfaced an important lesson: once the app is connected to a real model, the main failure mode is no longer "the classifier is fake", but "the model speaks natural language while the benchmark uses a fixed product taxonomy."

For that reason, the evaluation now distinguishes between:

- `strict normalized` accuracy: conservative comparison after canonicalizing labels
- `semantic relaxed` accuracy: taxonomy-aware matching that allows concept overlap such as `spring/summer` matching `summer`, or `sports bra` matching `bra`

Latest 10-image real-provider sanity-check results:

| Field | Strict normalized | Semantic relaxed |
| --- | --- | --- |
| `garment_type` | `90%` | `100%` |
| `style` | `100%` | `100%` |
| `occasion` | `70%` | `70%` |
| `season` | `30%` | `60%` |
| `base_colour` | `80%` | `80%` |

The takeaway is that the real model is materially stronger than the earlier placeholder classifier, but the benchmark still depends heavily on normalization and label design. In particular, `season` and `occasion` remain difficult because the dataset uses coarse retail labels while the model often returns richer or overlapping concepts.

### Benchmark Progression: Mock to Real Provider

The project evolved in three clear stages:

1. `Workflow-first integration`
   The first goal was to prove the product workflow end to end: upload, classify, persist, search, filter, annotate, and evaluate.
2. `Real-provider integration`
   Once the workflow and benchmark were stable, I connected the real multimodal provider through the existing abstraction layer. This validated the service boundaries without forcing a rewrite of the app.
3. `Semantic evaluation refinement`
   As soon as the real model was active, it became clear that many "errors" were really taxonomy mismatches rather than vision failures. That led to the addition of strict normalized scoring and semantic relaxed scoring.

This progression was useful because it separated three different questions:

- Does the system work end to end?
- Can a real model be plugged into the same architecture?
- How should model quality be measured once the output becomes more natural-language and less taxonomy-bound?

### Real-Provider Evaluation Progression

| Sample size | Strict garment | Strict style | Strict occasion | Strict season | Strict colour | Semantic garment | Semantic style | Semantic occasion | Semantic season | Semantic colour |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `10` | `90%` | `100%` | `70%` | `30%` | `80%` | `100%` | `100%` | `70%` | `60%` | `80%` |
| `50` | `42%` | `70.59%` | `66%` | `50%` | `82%` | `56%` | `70.59%` | `80%` | `58%` | `82%` |
| `100` | `43%` | `78.12%` | `56%` | `48%` | `87%` | `52%` | `78.12%` | `74%` | `54%` | `87%` |

A few patterns held up as the sample size increased:

- `base_colour` remained the most stable attribute once palette outputs were collapsed into canonical colors
- `occasion` improved substantially under semantic scoring, which suggests many misses were label-taxonomy mismatches rather than true model failures
- `garment_type` was hurt by retail taxonomy boundaries such as `Tops` vs `T-shirt`, even when the underlying concept was visually correct
- `season` remained the least stable field because both the dataset and the model naturally allow overlapping answers

## Labeling Rules For Fast Manual Evaluation

To keep the evaluation realistic and timeboxed, the benchmark focuses on the fields that are both useful and directly supported by the selected dataset:

- `garment_type`
- `style`
- `occasion`
- `season`
- `base_colour`

Practical guidance:

- Leave a field blank rather than guessing if the image is too ambiguous
- Treat `garment_type` as the most objective baseline field
- Expect `style` and `occasion` to have more disagreement
- Avoid using `consumer_profile`, `trend_notes`, or `location context` as gold-label fields unless there is unusually clear evidence

## Testing

Current automated coverage includes:

- unit tests for classification parsing defaults and normalization
- API tests for upload, image listing, filtering, and annotations
- evaluation-summary tests for accuracy aggregation
- a Playwright happy-path test for upload, classify, and filter
- a GitHub Actions workflow that runs backend tests and a frontend production build on push / PR

## UX Notes

### Large image libraries

If the library grew substantially beyond the current proof-of-concept size, the next user-experience improvements would be:

- image lazy loading
- pagination or infinite scroll
- skeleton states for library cards
- more explicit server-side loading placeholders

### Slow classifier responses

The current upload flow already provides an in-progress button state and completion feedback. If the classifier were replaced with a slower real model, the next improvements would be:

- explicit classify-in-progress states per upload
- background job status polling
- progress messaging for upload vs classification
- delayed placeholder cards so the library feels responsive immediately

## What Works Today

- Browser-based image upload
- Local image persistence
- Real image thumbnails in the library
- Placeholder classification and metadata persistence
- Optional real-provider path through the same classification interface
- Live image listing
- Search and dynamic filter flows
- Designer note annotations
- Evaluation scaffold and reporting generation

## Known Limitations

- A deployed real-model demo requires a valid API key and budget controls
- Images are stored locally instead of in cloud object storage
- Search is lexical and metadata-based, not embedding-based
- No auth or multi-user workflow is implemented
- The current benchmark uses source dataset labels plus light field mapping, not a custom annotation workflow built from scratch

## Product and Model Caveats

Some target attributes are much more subjective than others.

More visually grounded fields:

- `garment_type`
- parts of `pattern`
- some color-related attributes

Less reliable or more subjective fields:

- `material`
- `occasion`
- `consumer_profile`
- `trend_notes`
- `location context`

For that reason, the product is designed to treat AI output as a searchable suggestion layer, not as authoritative truth.

## Error Analysis

The real-provider benchmarks revealed a second layer of issues that only becomes visible once the model is actually grounded in the image:

- The model often predicts the right concept but not the exact dataset label, such as `Top / T-shirt` vs `Tops`
- `season` is especially sensitive to label granularity because the dataset often expects a single season while the model naturally returns `spring/summer` or `all seasons`
- `occasion` remains partly subjective and sometimes reflects a true semantic disagreement rather than a normalization miss
- `base_colour` becomes much more reliable once palette outputs are collapsed into canonical colors

That experience changed the evaluation design: instead of relying only on exact string matching, the benchmark now reports both conservative normalized scores and a more realistic taxonomy-aware semantic score for the real-model sanity check.

## Lessons From Real-Model Integration

- A workflow-first implementation is enough to validate the app architecture, but not enough to validate the evaluation design
- Real multimodal output quickly exposes taxonomy mismatches between natural-language descriptions and product-dataset labels
- Provider abstraction paid off: the real model could be plugged in without changing the upload, persistence, search, or annotation flows
- Normalization matters almost as much as prompt quality for structured attribute benchmarks
- Some fields, especially `season` and `occasion`, are as much a labeling problem as a modeling problem
- Running the same benchmark at `10`, `50`, and `100` samples is useful because it separates small-sample optimism from more stable medium- and full-scale behavior

## If I Had More Time

- Make the real multimodal provider the default runtime path in deployed environments
- Expand filters to additional metadata dimensions
- Add richer search, including embedding-based retrieval
- Add a dedicated annotation review pass on top of the current 100-image benchmark
- Refine the evaluation taxonomy so subjective fields have clearer semantic scoring rules
- Use designer notes as an additional retrieval signal and as feedback for future model refinement

## Submission Status

This repository now includes the core end-to-end workflow, automated tests, 10/50/100-image real-model benchmarks, deployment starter configuration, and submission-ready documentation. The largest remaining improvements would be production-grade storage, managed database infrastructure, and richer retrieval beyond lexical search.
