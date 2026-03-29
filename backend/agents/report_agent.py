"""
OrchestrAI - Report Agent
Generates weekly/monthly reports with AI-powered insights.
"""
import json
from datetime import datetime
from agents.base_agent import BaseAgent


class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Report Agent",
            system_instruction="""You are a Report Generation Agent. Create comprehensive,
            professional team/project reports with insights and recommendations."""
        )

    async def generate(self, report_data: dict, report_type: str = "weekly") -> dict:
        """Generate a structured report."""
        prompt = f"""Generate a {report_type} report from this data:

REPORT DATA:
{json.dumps(report_data, indent=2)}

Return JSON with:
- "title": string
- "executive_summary": string (3-4 sentences)
- "metrics": {{"tasks_completed": int, "tasks_pending": int, "tasks_delayed": int, "completion_rate": float, "team_health": "good|fair|poor"}}
- "highlights": ["highlight1"]
- "concerns": ["concern1"]
- "recommendations": ["rec1"]
- "detailed_sections": [{{"title": "Section Title", "content": "section content"}}]"""

        result = await self._call_gemini_json(prompt)
        if result and "executive_summary" in result:
            return result

        return self._demo_report(report_data, report_type)

    def _demo_report(self, data: dict, report_type: str) -> dict:
        tasks = data.get("tasks", [])
        completed = sum(1 for t in tasks if t.get("status") == "completed")
        delayed = sum(1 for t in tasks if t.get("status") == "delayed")
        pending = sum(1 for t in tasks if t.get("status") == "pending")
        in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
        total = len(tasks) or 1
        completion_rate = (completed / total) * 100

        team_name = data.get("team_name", "Team")
        project_name = data.get("project_name", "Project")

        health = "good" if completion_rate >= 70 else ("fair" if completion_rate >= 40 else "poor")

        return {
            "title": f"{team_name} {report_type.capitalize()} Report - {datetime.now().strftime('%B %Y')}",
            "executive_summary": f"The {team_name} completed {completed} out of {total} tasks this period ({completion_rate:.0f}% completion rate). {delayed} tasks experienced delays. Overall team health is {health}. {'The team is performing well and on track.' if health == 'good' else 'Some areas need attention to maintain project timelines.'}",
            "metrics": {
                "tasks_completed": completed,
                "tasks_pending": pending,
                "tasks_in_progress": in_progress,
                "tasks_delayed": delayed,
                "completion_rate": round(completion_rate, 1),
                "team_health": health
            },
            "highlights": [
                f"{completed} tasks completed successfully",
                "Team collaboration remains strong",
                "Key milestones achieved this period"
            ],
            "concerns": [
                f"{delayed} tasks delayed" if delayed > 0 else "No significant delays",
                "Resource allocation needs review" if health != "good" else "Resource utilization is optimal"
            ],
            "recommendations": [
                "Continue current momentum on high-priority items",
                "Address delayed tasks with additional resources" if delayed > 0 else "Maintain current pace",
                "Schedule team retrospective to identify process improvements"
            ],
            "detailed_sections": [
                {"title": "Task Breakdown", "content": f"Completed: {completed} | In Progress: {in_progress} | Pending: {pending} | Delayed: {delayed}"},
                {"title": "Team Performance", "content": f"Completion rate: {completion_rate:.0f}%. Team health: {health}."},
                {"title": "Next Period Goals", "content": "Focus on clearing pending tasks and resolving delayed items."}
            ]
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_report({}, "weekly"))
