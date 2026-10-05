"""app/schemas/summary_schema.py - Pydantic models for multi-document synthesis."""

from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class SummaryMode(str, Enum):
    EXECUTIVE = "executive"
    ACTIONABLE = "actionable"
    COMPARATIVE = "comparative"
    COMPREHENSIVE = "comprehensive"


class DetailLevel(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    DETAILED = "detailed"


class ActionItem(BaseModel):
    action: str = Field(..., example="Audit cloud EC2 instance reserve capacity")
    owner: str = Field(default="Unassigned", example="DevOps / Engineering")
    priority: str = Field(default="Medium", example="High")


class TextSummarizationRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, description="List of raw text documents to summarize")
    mode: SummaryMode = Field(default=SummaryMode.EXECUTIVE, example=SummaryMode.EXECUTIVE)
    detail_level: DetailLevel = Field(default=DetailLevel.MEDIUM, example=DetailLevel.MEDIUM)
    focus_topic: Optional[str] = Field(None, example="Financial growth and infrastructure costs")


class DocumentSummaryResponse(BaseModel):
    summary_id: str = Field(..., example="SUM-A1B2C3D4")
    mode: SummaryMode
    detail_level: DetailLevel
    documents_analyzed: List[str]
    total_characters_processed: int
    executive_summary: str
    key_findings: List[str]
    action_items: List[ActionItem]
    cross_document_insights: List[str]
    execution_time_ms: float
    engine_mode: str = Field(..., example="Map-Reduce Engine (Deterministic Mock)")