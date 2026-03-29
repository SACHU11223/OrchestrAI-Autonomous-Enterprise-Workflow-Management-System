"""
OrchestrAI - Risk Prediction Agent
Predicts project risks based on team data and metrics.
"""
import json
from agents.base_agent import BaseAgent


class RiskPredictionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Risk Prediction Agent",
            system_instruction="""You are a Risk Prediction Agent. Analyze project data to predict
            potential risks including delivery delays, resource issues, and quality concerns."""
        )

    async def predict(self, project_data: dict) -> dict:
        """Predict project risks."""
        prompt = f"""Analyze project risks:

PROJECT DATA:
{json.dumps(project_data, indent=2)}

Return JSON with:
- "overall_risk_level": "low" | "medium" | "high" | "critical"
- "risk_score": float 0-100
- "risks": [{{"category": "delivery|resource|quality|technical", "description": "risk description", "probability": float 0-1, "impact": "low|medium|high", "mitigation": "suggestion"}}]
- "risk_trend": "improving" | "stable" | "worsening"
- "summary": string"""

        result = await self._call_gemini_json(prompt)
        if result and "overall_risk_level" in result:
            return result

        return self._demo_risks(project_data)

    def _demo_risks(self, data: dict) -> dict:
        tasks = data.get("tasks", [])
        delayed = sum(1 for t in tasks if t.get("status") == "delayed")
        total = len(tasks) or 1
        delay_rate = delayed / total

        risks = []
        risk_score = 20  # Base risk

        if delay_rate > 0.2:
            risks.append({"category": "delivery", "description": "High task delay rate threatens project timeline", "probability": min(0.9, delay_rate + 0.3), "impact": "high", "mitigation": "Reallocate resources and adjust timeline"})
            risk_score += 30

        feedback = data.get("feedback", [])
        neg_feedback = sum(1 for f in feedback if f.get("sentiment") == "negative")
        if neg_feedback > len(feedback) * 0.3 if feedback else False:
            risks.append({"category": "resource", "description": "Team morale concerns may impact productivity", "probability": 0.6, "impact": "medium", "mitigation": "Conduct 1-on-1 meetings and address concerns"})
            risk_score += 20

        if not risks:
            risks.append({"category": "delivery", "description": "Standard project delivery risk", "probability": 0.2, "impact": "low", "mitigation": "Continue regular monitoring"})

        risk_score = min(100, risk_score)
        level = "critical" if risk_score >= 75 else ("high" if risk_score >= 50 else ("medium" if risk_score >= 25 else "low"))

        return {
            "overall_risk_level": level,
            "risk_score": risk_score,
            "risks": risks,
            "risk_trend": "worsening" if delay_rate > 0.3 else ("stable" if delay_rate > 0.1 else "improving"),
            "summary": f"Project risk score: {risk_score}/100. {len(risks)} risk(s) identified. {'Immediate attention required.' if risk_score >= 50 else 'Continue monitoring.'}"
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_risks({}))
