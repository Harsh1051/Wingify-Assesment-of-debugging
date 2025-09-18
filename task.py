"""
Task runner for analyzing a financial document file.

This module provides `analyze_document(path)` which extracts text from the PDF
and forwards it to the analysis tools.
"""
import os

def analyze_document(path: str) -> dict:
    if not os.path.exists(path):
        return {"error": "file not found", "path": path}

    # Try to extract text using PyPDF2; if not available or extraction fails,
    # fall back to returning a short error-friendly message.
    text = ""
    try:
        import PyPDF2
        with open(path, "rb") as fh:
            reader = PyPDF2.PdfReader(fh)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        # If pdf text extraction fails, return an error message rather than crash.
        return {"error": "failed to extract text from PDF", "exception": str(e)}

    # If no text was found, return a helpful message
    if not text.strip():
        return {"error": "no extractable text found in PDF"}

    # Use the analysis tool to produce structured output
    try:
        from tools import FinancialDocumentTool
        tool = FinancialDocumentTool()
        result = tool.analyze(text, filename=os.path.basename(path))
        return {"analysis": result}
    except Exception as e:
        return {"error": "analysis tool failed", "exception": str(e)}
