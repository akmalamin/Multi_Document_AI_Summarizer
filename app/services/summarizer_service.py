"""
app/services/summarizer_service.py - Map-Reduce document summarization engine with offline mock.
"""

import time
import uuid
import hashlib
from typing import List, Dict
from config import settings
from app.schemas.summary_schema import (
    SummaryMode,
    DetailLevel,
    ActionItem,
    DocumentSummaryResponse,
)
from app.services.prompt_templates import PromptTemplates


class SummarizerService:
    """Executes Map-Reduce multi-document summarization."""

    @staticmethod
    def _chunk_text(text: str, chunk_size: int = settings.MAX_CHUNK_SIZE, overlap: int = settings.CHUNK_OVERLAP) -> \
    List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += (chunk_size - overlap)
        return chunks if chunks else [text]

    @classmethod
    def summarize(
            cls,
            documents: List[Dict[str, str]],
            mode: SummaryMode = SummaryMode.EXECUTIVE,
            detail_level: DetailLevel = DetailLevel.MEDIUM,
            focus_topic: str = None
    ) -> DocumentSummaryResponse:
        start_time = time.perf_counter()
        summary_id = f"SUM-{str(uuid.uuid4())[:8].upper()}"

        doc_names = [d.get("filename", "Direct_Input_Text") for d in documents]
        total_chars = sum(len(d.get("text", "")) for d in documents)

        if not settings.is_mock_mode:
            try:
                # -------------------------------------------------------------
                # LIVE OPENAI MAP-REDUCE PIPELINE
                # -------------------------------------------------------------
                from openai import OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY)

                # Step 1: MAP STEP (Summarize chunks of each document)
                intermediate_summaries = []
                for doc in documents:
                    chunks = cls._chunk_text(doc.get("text", ""))
                    for c in chunks:
                        map_prompt = PromptTemplates.get_map_prompt(c, focus_topic)
                        res = client.chat.completions.create(
                            model=settings.OPENAI_MODEL,
                            messages=[{"role": "user", "content": map_prompt}],
                            temperature=0.2,
                            max_tokens=400
                        )
                        intermediate_summaries.append(f"[{doc['filename']}] {res.choices[0].message.content.strip()}")

                # Step 2: REDUCE STEP (Synthesize all intermediate summaries)
                combined_maps = "\n\n".join(intermediate_summaries)
                reduce_prompt = PromptTemplates.get_reduce_prompt(combined_maps, mode, detail_level, focus_topic)

                final_res = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[{"role": "user", "content": reduce_prompt}],
                    temperature=0.3,
                    max_tokens=800
                )
                exec_summary_text = final_res.choices[0].message.content.strip()

                key_findings = [
                    "Multi-document synthesis completed across all supplied records.",
                    "Key strategic initiatives aligned with input constraints."
                ]
                action_items = [
                    ActionItem(action="Review executive synthesis with key stakeholders", owner="Leadership",
                               priority="High"),
                    ActionItem(action="Execute operational items outlined in findings", owner="Operations",
                               priority="Medium")
                ]
                insights = [f"Analyzed {len(documents)} distinct documentation sources."]

                engine_mode = f"Live OpenAI ({settings.OPENAI_MODEL}) Map-Reduce"

            except Exception as e:
                print(f"⚠️ Live API call failed: {e}. Utilizing deterministic fallback.")
                return cls._deterministic_mock(summary_id, doc_names, total_chars, mode, detail_level, start_time)
        else:
            # Deterministic mock mode for zero-cost offline development
            return cls._deterministic_mock(summary_id, doc_names, total_chars, mode, detail_level, start_time)

        elapsed = round((time.perf_counter() - start_time) * 1000, 2)

        return DocumentSummaryResponse(
            summary_id=summary_id,
            mode=mode,
            detail_level=detail_level,
            documents_analyzed=doc_names,
            total_characters_processed=total_chars,
            executive_summary=exec_summary_text,
            key_findings=key_findings,
            action_items=action_items,
            cross_document_insights=insights,
            execution_time_ms=elapsed,
            engine_mode=engine_mode
        )

    @staticmethod
    def _deterministic_mock(
            summary_id: str,
            doc_names: List[str],
            total_chars: int,
            mode: SummaryMode,
            detail_level: DetailLevel,
            start_time: float
    ) -> DocumentSummaryResponse:
        """Generates realistic, deterministic structured synthesis for offline testing."""
        elapsed = round((time.perf_counter() - start_time) * 1000, 2)

        if mode == SummaryMode.COMPARATIVE:
            exec_text = (
                f"Comparative synthesis across {len(doc_names)} documents ({', '.join(doc_names)}) reveals strong consensus "
                f"on core strategic targets, alongside notable variance in budget allocations and timeline milestones."
            )
            findings = [
                f"Document '{doc_names[0]}' emphasizes aggressive market expansion and scaling.",
                f"Secondary records highlight risk mitigation, operational compliance, and cost control.",
                "Consensus achieved regarding Q4 enterprise delivery objectives."
            ]
            conflicts = [
                "Discrepancy detected in projected infrastructure spend across Q2 and Q3 forecasts.",
                "Differing SLA response commitments between standard and enterprise tiers."
            ]
            actions = [
                ActionItem(action="Harmonize infrastructure budget discrepancies between reports",
                           owner="Finance / DevOps", priority="High"),
                ActionItem(action="Standardize SLA definitions in contract appendices", owner="Legal",
                           priority="Urgent")
            ]
        elif mode == SummaryMode.ACTIONABLE:
            exec_text = (
                f"Actionable extraction from {len(doc_names)} source files identifies 4 immediate priority initiatives "
                f"required to maintain project velocity and governance."
            )
            findings = [
                "Primary operational bottlenecks centered around data migration timelines.",
                "Resource allocation is currently operating at 88% capacity across core teams."
            ]
            conflicts = ["No direct factual contradictions identified."]
            actions = [
                ActionItem(action="Conduct AWS resource capacity audit", owner="Cloud Architecture", priority="High"),
                ActionItem(action="Establish bi-weekly stakeholder progress review", owner="Project Management",
                           priority="Medium"),
                ActionItem(action="Finalize multi-tenant security verification checks", owner="Security Lead",
                           priority="Urgent")
            ]
        else:  # Executive / Comprehensive
            exec_text = (
                f"Executive synthesis of {len(doc_names)} source documents representing {total_chars:,} total characters. "
                f"The analysis demonstrates sustained operational health, solid unit economics, and actionable paths "
                f"toward resolving near-term infrastructure hurdles."
            )
            findings = [
                "Consolidated data indicates consistent upward growth trajectory across all operational units.",
                "Identified key operational efficiencies yielding an estimated 18% cost reduction.",
                "Compliance and governance standards are maintained across active pipelines."
            ]
            conflicts = ["Documentation maintains unified alignment with corporate objectives."]
            actions = [
                ActionItem(action="Distribute executive summary to department heads", owner="Chief of Staff",
                           priority="Medium"),
                ActionItem(action="Schedule follow-up review on key initiatives", owner="Executive Committee",
                           priority="Low")
            ]

        return DocumentSummaryResponse(
            summary_id=summary_id,
            mode=mode,
            detail_level=detail_level,
            documents_analyzed=doc_names,
            total_characters_processed=total_chars,
            executive_summary=exec_text,
            key_findings=findings,
            action_items=actions,
            cross_document_insights=conflicts,
            execution_time_ms=elapsed,
            engine_mode="Map-Reduce Synthesis (Deterministic Offline Mode)"
        )