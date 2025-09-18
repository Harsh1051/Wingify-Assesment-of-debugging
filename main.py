from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import uuid

from task import analyze_document

app = FastAPI(title="Financial Document Analyzer (Debugged)")

BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """Accepts a PDF file upload and returns a JSON analysis.

    This endpoint saves the uploaded file to the outputs directory and
    runs the document analysis routine from task.analyze_document.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    job_id = str(uuid.uuid4())
    dest = os.path.join(OUTPUT_DIR, f"{job_id}_{file.filename}")
    content = await file.read()
    with open(dest, "wb") as fh:
        fh.write(content)

    # Run the analysis (synchronously for this debug assignment)
    analysis_result = analyze_document(dest)

    return {"job_id": job_id, "filename": file.filename, "result": analysis_result}
