"""
main.py - FastAPI Application Factory & Startup.
Run: uvicorn main:app --reload --port 8000
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from app.routers import health_router, summary_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount API Routers
app.include_router(health_router.router)
app.include_router(summary_router.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "docs": f"http://localhost:8000{settings.DOCS_URL}",
        "summarize_text_endpoint": "POST /api/v1/summary/text",
        "summarize_upload_endpoint": "POST /api/v1/summary/upload"
    }


if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════════════════╗
║   📑 MULTI-DOCUMENT AI SUMMARIZATION ENGINE — Day 134   ║
║   Interactive Swagger Docs: http://localhost:8000/docs   ║
╚══════════════════════════════════════════════════════════╝
    """)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)