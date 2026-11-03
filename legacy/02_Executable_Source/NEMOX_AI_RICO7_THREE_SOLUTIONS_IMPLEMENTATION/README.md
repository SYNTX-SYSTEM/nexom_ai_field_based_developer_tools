# nemox RICO-7 Three Field-Based Developer Tools

Independent reference implementations for a freight-forwarding hackathon. No affiliation or access to nemox internal systems is claimed.

## Run

From repository root: `docker compose up --build`

API documentation: http://localhost:8011/docs, http://localhost:8012/docs, http://localhost:8013/docs.

Run frontends independently: `cd <solution>/frontend && npm install && npm run dev`. Vite ports: 9011, 9012, 9013.

Local Python: `pip install -r <solution>/requirements.txt`; `PYTHONPATH=shared uvicorn backend.main:app --port <solution_port>` from each solution directory.

Tests: `cd <solution> && PYTHONPATH=.:../shared pytest -q`.

## Demonstrations

A: POST /api/analyze with `{"request":"Same shipment as last week, but two days earlier."}`.
B: POST /api/decisions, POST /api/feedback, POST /api/confirm, POST /api/compare.
C: POST /api/gaps/analyze, POST /api/gaps/resolve.

## Boundaries

These are functional prototype implementations with synthetic data. They do not include production identity management, event-stream concurrency, operational TMS integration, or a real LLM provider. React interfaces are lightweight inspection shells.
