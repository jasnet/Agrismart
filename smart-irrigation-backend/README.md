Smart Irrigation Backend (FastAPI + SQLite)

Run locally:
1. python -m venv venv
2. source venv/bin/activate # or venv\Scripts\activate on Windows
3. pip install -r requirements.txt
4. export ENV=dev # optional
5. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

API docs: http://localhost:8000/docs

This app provides endpoints to manage fields, push sensor readings, and compute schedules for fields.
