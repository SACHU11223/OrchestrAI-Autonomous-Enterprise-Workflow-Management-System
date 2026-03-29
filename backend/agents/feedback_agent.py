"""
OrchestrAI - Feedback Agent
Processes and analyzes daily employee updates.
"""
import json
from agents.base_agent import BaseAgent


class FeedbackAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Feedback Agent",
            system_instruction="""You are a Feedback Analysis Agent. Process daily employee updates
            to extract key information about progress, blockers, and actionable insights for managers."""
        )

    async def analyze(self, feedback_text: str, employee_name: str = "", sentiment: dict = None) -> dict:
        """Analyze employee feedback and provide insights."""
        sentiment_context = json.dumps(sentiment) if sentiment else "No sentiment data"
        prompt = f"""Analyze this employee's daily update:

EMPLOYEE: {employee_name or 'Unknown'}
UPDATE: {feedback_text}
SENTIMENT DATA: {sentiment_context}

Return JSON with:
- "progress_summary": string (what was accomplished)
- "blockers": ["blocker1"] or empty
- "needs_attention": boolean
- "manager_action_items": ["action1"] or empty
- "follow_up_priority": "low" | "medium" | "high"
- "coaching_suggestions": string"""

        result = await self._call_gemini_json(prompt)
        if result and "progress_summary" in result:
            return result

        return self._demo_analysis(feedback_text, sentiment)

    def _demo_analysis(self, text: str, sentiment: dict = None) -> dict:
        text_lower = text.lower()
        sent = sentiment or {}
        is_negative = sent.get("sentiment") == "negative"
        
        blockers = []
        if any(w in text_lower for w in ["blocked", "stuck", "waiting", "need", "cannot"]):
            blockers.append("Technical or resource blocker identified")
        if any(w in text_lower for w in ["help", "support", "unclear", "confused"]):
            blockers.append("Needs additional guidance or support")

        actions = []
        if is_negative:
            actions.append("Schedule 1-on-1 to discuss concerns")
        if blockers:
            actions.append("Help resolve identified blockers")
        if any(w in text_lower for w in ["delay", "behind", "late"]):
            actions.append("Review and adjust timeline if needed")

        return {
            "progress_summary": "Employee provided status update on current work items.",
            "blockers": blockers,
            "needs_attention": is_negative or len(blockers) > 0,
            "manager_action_items": actions if actions else ["No immediate action required"],
            "follow_up_priority": "high" if is_negative else ("medium" if blockers else "low"),
            "coaching_suggestions": "Provide positive reinforcement and clear priorities." if not is_negative else "Offer support and reduce scope if possible."
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_analysis(prompt))
