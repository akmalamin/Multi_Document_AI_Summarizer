"""app/services/document_loader.py - Multi-format PDF and TXT text extractor."""

import os
from pypdf import PdfReader
from typing import List, Dict


class DocumentLoader:
    """Extracts clean text and metadata from uploaded PDFs and text files."""

    @staticmethod
    def load_pdf(pdf_path: str) -> Dict[str, str]:
        filename = os.path.basename(pdf_path)
        try:
            reader = PdfReader(pdf_path)
            extracted_pages = []
            for idx, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""
                page_text = " ".join(page_text.split())
                if page_text:
                    extracted_pages.append(f"[Page {idx}] {page_text}")

            full_text = "\n\n".join(extracted_pages)
            return {"filename": filename, "text": full_text, "pages": len(reader.pages)}
        except Exception as e:
            return {"filename": filename, "text": "", "error": str(e), "pages": 0}

    @staticmethod
    def load_txt(txt_path: str) -> Dict[str, str]:
        filename = os.path.basename(txt_path)
        try:
            with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return {"filename": filename, "text": " ".join(content.split()), "pages": 1}
        except Exception as e:
            return {"filename": filename, "text": "", "error": str(e), "pages": 0}