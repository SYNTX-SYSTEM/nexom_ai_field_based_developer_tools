# Recursive Feedback & Decision Trace Engine

Independent developer tool using shared field contracts.

Backend: `PYTHONPATH=.:../shared uvicorn backend.main:app --port 8012` from this project directory after `pip install -r requirements.txt`.
Frontend: `cd frontend && npm install && npm run dev` (port 9012).
Tests: `PYTHONPATH=.:../shared pytest -q`.
Swagger: http://localhost:8012/docs

Demo data is synthetic. SQLite DB is created on first launch.
