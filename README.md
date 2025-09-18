# 📄 Financial Document Analyzer – Debug Assignment  

## 📌 Overview  
This project is a **Financial Document Analyzer** built with **FastAPI**.  
It allows uploading a financial PDF, extracts insights (summary, key metrics, recommendations), and returns structured JSON.  

This repo contains the **debugged and fixed version** of the assignment.  

---

## ✅ What I Changed  
- Fixed broken/placeholder code with working implementations:
  - Added FastAPI server (`main.py`) with `/analyze` and `/health` endpoints.  
  - Implemented PDF text extraction (`task.py`, `tools.py`).  
  - Added deterministic analysis logic with safe fallbacks.  
- Improved CrewAI prompts for more structured and relevant output.  
- Validated and filtered extracted numbers to avoid garbage values.  
- Standardized job ID & filename handling (`{job_id}_{original_filename}`).  

---

## ⚡ Setup Instructions  

### 1. Clone the Repository  
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name> 


### 2. Create Virtual Environment
python -m venv .venv
source .venv/Scripts/activate   # Windows  
# or  
source .venv/bin/activate       # Linux/Mac

3. Install Dependencies
pip install -r requirements.txt


Minimal run works with:

pip install fastapi "uvicorn[standard]" PyPDF2

4. Run the Server
uvicorn main:app --reload

Server runs at:
👉 http://127.0.0.1:8000

Swagger docs:
👉 http://127.0.0.1:8000/docs


🚀 API Documentation
POST /analyze

Input: PDF file (file in form-data).

Output: JSON with summary, metrics, and recommendation.

Example (cURL):

curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@data/TSLA-Q2-2025-Update.pdf;type=application/pdf'

Sample Response:

{
  "job_id": "59d42021-d6b6-4e44-b2de-cc927abf9c55",
  "filename": "TSLA-Q2-2025-Update.pdf",
  "result": {
    "analysis": {
      "filename": "59d42021-d6b6-4e44-b2de-cc927abf9c55_TSLA-Q2-2025-Update.pdf",
      "summary": "Q2 2025 Update Highlights...",
      "word_count": 7408,
      "top_numbers": [2025, 0.9, 1.2, 1.4],
      "recommendation": "HOLD (no clear signal)"
    }
  }
}


GET /health

Simple health check endpoint.

{ "status": "ok" }



🐛 Bugs Fixed

File Upload Bug → Fixed UploadFile handling with proper .read().

Inefficient Prompts → Rewritten for structured outputs.

Random/Nonsense Numbers → Filtered and validated results.

Job ID & Filename Mismatch → Standardized {job_id}_{filename} format.


📂 Included Sample Data

data/TSLA-Q2-2025-Update.pdf – Example PDF for testing.


🔮 Future Improvements (Optional)

Add Redis/Celery for background job queue.

Database integration (SQLite/Postgres).

Plug CrewAI in tools.py for advanced LLM analysis.










