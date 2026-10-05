# 📑 Multi-Document AI Summarization & Synthesis Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Architecture: Map--Reduce](https://img.shields.io/badge/Architecture-Map--Reduce-purple.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise multi-document AI synthesis engine built with **FastAPI**, **PyPDF**, and **OpenAI GPT**. Implements Map-Reduce chunking to compress large multi-page reports, extract actionable tasks with owner tags, identify cross-document conflicts, and output executive briefings.

---

## 🌟 Key Capabilities

- **📚 Multi-Document Ingestion:** Ingests multiple PDF and TXT files simultaneously.
- **🗺️ Map-Reduce Pipeline:** Summarizes long texts in chunks before running final synthesis to prevent context overflow.
- **🎯 4 Summarization Modes:**
  - `executive`: High-impact 1-paragraph overview.
  - `actionable`: Bulleted takeaways and prioritized Action Item matrix.
  - `comparative`: Highlights cross-document consensus vs. discrepancies.
  - `comprehensive`: Deep, structured section-by-section breakdown.
- **🧪 Deterministic Offline Fallback:** Fully operational for zero-cost development out-of-the-box.

---

## 🚀 Quick Start

```bash
# 1. Setup Environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Run Server
uvicorn main:app --reload --port 8000