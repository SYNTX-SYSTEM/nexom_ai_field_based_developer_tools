# User Intent & Context Inspector

Independent developer tool using shared field contracts.

Backend: `PYTHONPATH=.:../shared uvicorn backend.main:app --port 8011` from this project directory after `pip install -r requirements.txt`.
Frontend: `cd frontend && npm install && npm run dev` (port 9011).
Tests: `PYTHONPATH=.:../shared pytest -q`.
Swagger: http://localhost:8011/docs

Demo data is synthetic. SQLite DB is created on first launch.
