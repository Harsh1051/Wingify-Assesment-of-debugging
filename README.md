# Financial Document Analyzer - Debug Assignment (Fixed)

## What I changed
- Replaced broken/placeholder code with working implementations that:
  - Provide a minimal FastAPI server (`main.py`) with a `/analyze` POST endpoint.
  - Implement PDF text extraction and deterministic analysis logic (`task.py`, `tools.py`).
  - Provide safe fallbacks when external LLMs (CrewAI) or PDF libraries are not available.

- The repo is now runnable locally and will return a deterministic JSON response for the included sample PDF.

## How to run (local)
1. Create a Python 3.10+ virtual environment and activate it.
2. Install dependencies (you can start with the minimal set for the debug run):
   ```
   pip install fastapi "uvicorn[standard]" PyPDF2
   ```
   - If you want to use CrewAI integration later, install the CrewAI packages and add required env vars.

3. Run the app:
   ```
   uvicorn financial-document-analyzer-debug.main:app --reload
   ```
   Then POST a PDF to `http://127.0.0.1:8000/analyze` using curl or Postman.

## API
### POST /analyze
- Accepts a single PDF file (form field `file`).
- Returns `job_id`, `filename`, and `result` (a structured analysis dict).

### GET /health
- Simple health check returning `{"status":"ok"}`

## Notes & Next steps
- Prompt improvements / CrewAI integration: `tools.py` has a `_analyze_with_llm` placeholder where CrewAI prompt engineering and model parameters can be added. Prefer returning strict JSON output via a schema (helps with determinism).
- Bonus: Queue workers + persistence can be added by introducing Redis + RQ/Celery and a database (SQLite/Postgres) to store job status and results. I can add this if you'd like.

## Included sample
- `data/TSLA-Q2-2025-Update.pdf` - a sample PDF used for testing.
