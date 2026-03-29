"""
OrchestrAI - Deadline Agent
Sets intelligent deadlines for tasks based on complexity, priority, and team capacity.
"""
import json
from datetime import datetime, timedelta
from agents.base_agent import BaseAgent


class DeadlineAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Deadline Agent",
            system_instruction="""You are a Deadline Setting Agent. Set realistic deadlines for tasks
            based on estimated hours, priority, task complexity, and team capacity.
            Consider buffer time for reviews and unexpected delays."""
        )

    async def set_deadlines(self, tasks: list, project_name: str = "") -> list:
        """Set deadlines for extracted tasks."""
        prompt = f"""Set realistic deadlines for these tasks. Today's date is {datetime.now().strftime('%Y-%m-%d')}.

PROJECT: {project_name}
TASKS:
{json.dumps(tasks, indent=2)}

For each task, add a "deadline" field in YYYY-MM-DD format.
Consider:
- Priority (critical = sooner, low = more buffer)
- Estimated hours (more hours = more time needed)
- Include 20% buffer for unexpected issues
Return the updated tasks array as JSON."""

        result = await self._call_gemini_json(prompt)
        if isinstance(result, list) and len(result) > 0:
            return result

        return self._demo_deadlines(tasks)

    def _demo_deadlines(self, tasks: list) -> list:
        """Set demo deadlines based on priority and estimated hours."""
        today = datetime.now()
        priority_days = {
            "critical": 3,
            "high": 7,
            "medium": 14,
            "low": 21
        }

        for task in tasks:
            priority = task.get("priority", "medium")
            est_hours = task.get("estimated_hours", 8)
            
            base_days = priority_days.get(priority, 14)
            # Add days based on estimated hours (1 day per 6 hours)
            work_days = max(1, int(est_hours / 6))
            total_days = base_days + work_days
            # Add 20% buffer
            total_days = int(total_days * 1.2)
            
            deadline = today + timedelta(days=total_days)
            # Skip weekends
            while deadline.weekday() >= 5:
                deadline += timedelta(days=1)
            
            task["deadline"] = deadline.strftime("%Y-%m-%d")

        return tasks

    def _fallback_response(self, prompt: str) -> str:
        return '[]'
