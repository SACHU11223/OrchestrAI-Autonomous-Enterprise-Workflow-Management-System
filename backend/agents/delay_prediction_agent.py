"""
OrchestrAI - Delay Prediction Agent
Predicts potential task delays based on feedback and historical data.
"""
import json
from agents.base_agent import BaseAgent


class DelayPredictionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Delay Prediction Agent",
            system_instruction="""You are a Delay Prediction Agent. Analyze task progress, employee feedback,
            and historical patterns to predict if a task is likely to be delayed."""
        )

    async def predict(self, feedback_text: str, task_title: str = "", sentiment: dict = None) -> dict:
        """Predict if a task will be delayed."""
        prompt = f"""Predict the delay probability for this task:

TASK: {task_title}
LATEST FEEDBACK: {feedback_text}
SENTIMENT: {json.dumps(sentiment) if sentiment else 'N/A'}

Return JSON with:
- "delay_probability": float 0-1
- "risk_level": "low" | "medium" | "high" | "critical"
- "predicted_delay_days": integer (0 if no delay expected)
- "risk_factors": ["factor1"]
- "mitigation_suggestions": ["suggestion1"]"""

        result = await self._call_gemini_json(prompt)
        if result and "delay_probability" in result:
            return result

        return self._demo_prediction(feedback_text, sentiment)

    def _demo_prediction(self, text: str, sentiment: dict = None) -> dict:
        text_lower = text.lower()
        score = 0.2  # Base delay probability

        risk_factors = []
        if any(w in text_lower for w in ["delay", "late", "behind", "slow"]):
            score += 0.25
            risk_factors.append("Direct delay indicators in feedback")
        if any(w in text_lower for w in ["complex", "difficult", "hard", "tricky"]):
            score += 0.15
            risk_factors.append("Task complexity concerns")
        if any(w in text_lower for w in ["blocked", "stuck", "waiting"]):
            score += 0.2
            risk_factors.append("Active blockers present")
        if sentiment and sentiment.get("sentiment") == "negative":
            score += 0.15
            risk_factors.append("Negative employee sentiment")

        score = min(1.0, score)
        
        if score >= 0.7:
            risk_level = "critical"
            delay_days = 7
        elif score >= 0.5:
            risk_level = "high"
            delay_days = 4
        elif score >= 0.3:
            risk_level = "medium"
            delay_days = 2
        else:
            risk_level = "low"
            delay_days = 0

        mitigations = []
        if "blocked" in text_lower or "stuck" in text_lower:
            mitigations.append("Escalate blockers immediately")
        if score > 0.5:
            mitigations.append("Consider reallocating resources")
            mitigations.append("Break task into smaller subtasks")
        if score > 0.3:
            mitigations.append("Increase check-in frequency")
        if not mitigations:
            mitigations.append("Continue monitoring progress")

        return {
            "delay_probability": round(score, 2),
            "risk_level": risk_level,
            "predicted_delay_days": delay_days,
            "risk_factors": risk_factors if risk_factors else ["No significant risk factors"],
            "mitigation_suggestions": mitigations
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_prediction(prompt))
