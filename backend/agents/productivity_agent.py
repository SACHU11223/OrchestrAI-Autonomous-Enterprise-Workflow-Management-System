"""
OrchestrAI - Productivity Agent
Calculates employee and team productivity scores.
"""
import json
from agents.base_agent import BaseAgent


class ProductivityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Productivity Agent",
            system_instruction="""You are a Productivity Analysis Agent. Calculate productivity scores
            based on task throughput, efficiency, and output quality."""
        )

    async def calculate(self, employee_data: dict) -> dict:
        """Calculate productivity score."""
        prompt = f"""Calculate productivity for this employee:

DATA:
{json.dumps(employee_data, indent=2)}

Return JSON with:
- "productivity_score": float 0-100
- "efficiency_rating": float 0-100
- "throughput_rate": float (tasks per week)
- "trend": "improving" | "stable" | "declining"
- "insights": ["insight1"]"""

        result = await self._call_gemini_json(prompt)
        if result and "productivity_score" in result:
            return result

        return self._demo_productivity(employee_data)

    def _demo_productivity(self, data: dict) -> dict:
        completed = data.get("tasks_completed", 0)
        total = data.get("tasks_total", 1) or 1
        delayed = data.get("tasks_delayed", 0)

        completion_rate = completed / total
        on_time_rate = (completed - delayed) / total if completed > delayed else completed / total
        
        productivity = (completion_rate * 60 + on_time_rate * 40)
        efficiency = on_time_rate * 100
        throughput = completed / 4  # Assuming monthly data = 4 weeks

        if productivity >= 80:
            trend = "improving"
            insights = ["High task completion rate", "Consistently meeting deadlines", "Consider stretch goals"]
        elif productivity >= 60:
            trend = "stable"
            insights = ["Steady performance", "Room for improvement in timeliness", "Focus on priority tasks"]
        else:
            trend = "declining"
            insights = ["Task completion needs improvement", "Consider workload adjustment", "May need additional support"]

        return {
            "productivity_score": round(productivity, 1),
            "efficiency_rating": round(efficiency, 1),
            "throughput_rate": round(throughput, 2),
            "trend": trend,
            "insights": insights
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_productivity({}))
