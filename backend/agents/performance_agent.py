"""
OrchestrAI - Performance Agent
Calculates employee performance scores.
"""
import json
from agents.base_agent import BaseAgent


class PerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Performance Agent",
            system_instruction="""You are a Performance Evaluation Agent. Calculate comprehensive
            performance scores based on task completion, quality, timeliness, and collaboration."""
        )

    async def calculate(self, employee_data: dict) -> dict:
        """Calculate performance score for an employee."""
        prompt = f"""Calculate a performance score for this employee:

EMPLOYEE DATA:
{json.dumps(employee_data, indent=2)}

Return JSON with:
- "performance_score": float 0-100
- "quality_score": float 0-100
- "timeliness_score": float 0-100
- "collaboration_score": float 0-100
- "strengths": ["strength1"]
- "improvement_areas": ["area1"]
- "overall_rating": "exceptional" | "exceeds_expectations" | "meets_expectations" | "needs_improvement"
- "recommendations": string"""

        result = await self._call_gemini_json(prompt)
        if result and "performance_score" in result:
            return result

        return self._demo_performance(employee_data)

    def _demo_performance(self, data: dict) -> dict:
        completed = data.get("tasks_completed", 0)
        total = data.get("tasks_total", 1) or 1
        delayed = data.get("tasks_delayed", 0)
        
        completion_rate = (completed / total) * 100
        delay_rate = (delayed / total) * 100
        
        timeliness = max(0, 100 - delay_rate * 2)
        quality = min(100, completion_rate * 1.1)
        collaboration = 75  # Default
        
        performance = (completion_rate * 0.4 + timeliness * 0.3 + quality * 0.2 + collaboration * 0.1)
        
        if performance >= 90:
            rating = "exceptional"
            strengths = ["Consistently delivers ahead of schedule", "High-quality output"]
            areas = ["Continue mentoring junior members"]
        elif performance >= 75:
            rating = "exceeds_expectations"
            strengths = ["Solid task completion rate", "Good team collaboration"]
            areas = ["Focus on reducing delays", "Take on stretch assignments"]
        elif performance >= 60:
            rating = "meets_expectations"
            strengths = ["Reliable team member", "Steady progress on tasks"]
            areas = ["Improve task completion speed", "Proactive communication"]
        else:
            rating = "needs_improvement"
            strengths = ["Shows potential for growth"]
            areas = ["Improve task completion rate", "Better time management", "Seek help earlier on blockers"]

        return {
            "performance_score": round(performance, 1),
            "quality_score": round(quality, 1),
            "timeliness_score": round(timeliness, 1),
            "collaboration_score": collaboration,
            "strengths": strengths,
            "improvement_areas": areas,
            "overall_rating": rating,
            "recommendations": f"Based on a {completion_rate:.0f}% completion rate with {delay_rate:.0f}% delays. {'Consider recognition or promotion.' if performance >= 90 else 'Focus on identified improvement areas.'}"
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_performance({}))
