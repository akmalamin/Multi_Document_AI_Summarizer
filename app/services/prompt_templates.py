"""app/services/prompt_templates.py - Map-Reduce and specialized summarization prompts."""

from app.schemas.summary_schema import SummaryMode, DetailLevel


class PromptTemplates:
    """Constructs tailored system and synthesis prompts based on target mode."""

    @staticmethod
    def get_map_prompt(chunk_text: str, focus_topic: str = None) -> str:
        focus_instruction = f"Focus particularly on aspects relating to: '{focus_topic}'." if focus_topic else ""
        return (
            f"You are an expert analytical reader.\n"
            f"Extract the core facts, metrics, risks, and conclusions from the text below.\n"
            f"{focus_instruction}\n"
            f"Be factual and concise.\n\n"
            f"TEXT CHUNK:\n{chunk_text}\n\n"
            f"CONCISE EXTRACTION:"
        )

    @staticmethod
    def get_reduce_prompt(all_summaries: str, mode: SummaryMode, detail_level: DetailLevel, focus_topic: str = None) -> str:
        focus_instruction = f"Prioritize insights regarding: '{focus_topic}'." if focus_topic else ""

        mode_instructions = {
            SummaryMode.EXECUTIVE: "Write a high-impact, 1-paragraph Executive Overview suitable for a CEO or Board.",
            SummaryMode.ACTIONABLE: "Extract clear, actionable Key Findings and concrete Action Items with recommended owners.",
            SummaryMode.COMPARATIVE: "Highlight key areas of consensus, discrepancies, and major differences across the source documents.",
            SummaryMode.COMPREHENSIVE: "Provide a detailed, section-by-section breakdown encompassing Background, Core Findings, and Strategic Next Steps."
        }

        return (
            f"You are an enterprise chief of staff synthesising multiple source reports.\n"
            f"{mode_instructions.get(mode, '')}\n"
            f"{focus_instruction}\n"
            f"Detail Level: {detail_level.value.upper()}\n\n"
            f"INTERMEDIATE EXTRACTED SUMMARIES:\n{all_summaries}\n\n"
            f"FINAL SYNTHESIS:"
        )