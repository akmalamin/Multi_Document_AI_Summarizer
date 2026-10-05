"""
app/routers/summary_router.py - Endpoints for Text & Multi-PDF Summarization.
"""

import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import List, Optional

from config import settings
from app.schemas.summary_schema import (
    SummaryMode,
    DetailLevel,
    TextSummarizationRequest,
    DocumentSummaryResponse,
)
from app.services.document_loader import DocumentLoader
from app.services.summarizer_service import SummarizerService

router = APIRouter(prefix="/summary", tags=["Multi-Document Summarization"])


@router.post("/text", response_model=DocumentSummaryResponse, status_code=status.HTTP_200_OK)
def summarize_raw_texts(request: TextSummarizationRequest):
    """
    Summarize one or multiple raw text blocks.
    Supports Executive, Actionable, Comparative, and Comprehensive modes.
    """
    documents = [{"filename": f"Text_Snippet_{i+1}", "text": t} for i, t in enumerate(request.texts)]
    return SummarizerService.summarize(
        documents=documents,
        mode=request.mode,
        detail_level=request.detail_level,
        focus_topic=request.focus_topic
    )


@router.post("/upload", response_model=DocumentSummaryResponse, status_code=status.HTTP_200_OK)
async def summarize_uploaded_files(
    files: List[UploadFile] = File(..., description="Upload up to 10 PDF or TXT files to synthesize"),
    mode: SummaryMode = Form(default=SummaryMode.EXECUTIVE),
    detail_level: DetailLevel = Form(default=DetailLevel.MEDIUM),
    focus_topic: Optional[str] = Form(default=None)
):
    """
    Upload multiple PDF/TXT files and generate a unified Map-Reduce executive synthesis.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    documents = []

    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in (".pdf", ".txt"):
            raise HTTPException(status_code=415, detail=f"Unsupported format: '{file.filename}'. Use PDF or TXT.")

        saved_path = os.path.join(settings.DOCS_INPUT_DIR, file.filename)
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if ext == ".pdf":
            doc_data = DocumentLoader.load_pdf(saved_path)
        else:
            doc_data = DocumentLoader.load_txt(saved_path)

        if doc_data.get("text"):
            documents.append(doc_data)

    if not documents:
        raise HTTPException(status_code=422, detail="No readable text could be extracted from uploaded files.")

    return SummarizerService.summarize(
        documents=documents,
        mode=mode,
        detail_level=detail_level,
        focus_topic=focus_topic
    )