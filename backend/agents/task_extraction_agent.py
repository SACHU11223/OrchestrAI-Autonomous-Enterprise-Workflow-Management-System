"""
OrchestrAI - Task Extraction Agent
Extracts actionable tasks from meeting transcripts.
"""
import json
import re
from agents.base_agent import BaseAgent


class TaskExtractionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Task Extraction Agent",
            system_instruction="""You are a Task Extraction Agent. Analyze meeting transcripts and summaries
            to extract specific, actionable tasks. For each task identify:
            - title: Clear, concise task title
            - description: Detailed task description
            - priority: low, medium, high, or critical
            - estimated_hours: Estimated time in hours
            - suggested_assignee: Name of the person mentioned, if any
            Return tasks as a JSON array."""
        )

    async def extract(self, transcript: str, summary: str = "") -> list:
        """Extract tasks from meeting transcript and summary."""
        prompt = f"""Extract all actionable tasks from this meeting:

TRANSCRIPT:
{transcript}

SUMMARY:
{summary}

Return a JSON array of tasks. Each task must have:
- "title": string (concise task title)
- "description": string (detailed description)
- "priority": "low" | "medium" | "high" | "critical"
- "estimated_hours": number
- "suggested_assignee": string (person's name or null)

Example: [{{"title": "Build login page", "description": "Create responsive login page with OAuth", "priority": "high", "estimated_hours": 8, "suggested_assignee": "John"}}]"""

        result = await self._call_gemini_json(prompt)
        if isinstance(result, list) and len(result) > 0:
            return result
        if isinstance(result, dict) and "tasks" in result:
            return result["tasks"]
        return self._generate_demo_tasks(transcript)

    def _generate_demo_tasks(self, transcript: str) -> list:
        """Generate demo tasks from transcript keywords."""
        text = transcript.lower()
        tasks = []

        # Pattern matching for common task indicators
        task_patterns = [
            (r"(?:need to|should|must|will|going to)\s+(.{10,60}?)(?:\.|,|$)", "high"),
            (r"(?:action item|task|todo|to-do):\s*(.{10,60}?)(?:\.|,|$)", "high"),
            (r"(?:work on|implement|build|create|design|develop)\s+(.{10,60}?)(?:\.|,|$)", "medium"),
        ]

        for pattern, priority in task_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:3]:
                title = match.strip().capitalize()
                if len(title) > 10:
                    tasks.append({
                        "title": title[:80],
                        "description": f"Task extracted from meeting: {title}",
                        "priority": priority,
                        "estimated_hours": 8,
                        "suggested_assignee": None
                    })

        # If no patterns found, generate generic tasks
        if not tasks:
            tasks = [
                {"title": "Review and prioritize sprint items", "description": "Review all items discussed in the meeting and prioritize for the current sprint.", "priority": "high", "estimated_hours": 4, "suggested_assignee": None},
                {"title": "Resolve identified blockers", "description": "Address technical blockers identified during the meeting.", "priority": "critical", "estimated_hours": 8, "suggested_assignee": None},
                {"title": "Update project documentation", "description": "Update project docs with decisions and action items from the meeting.", "priority": "medium", "estimated_hours": 3, "suggested_assignee": None},
                {"title": "Schedule follow-up review", "description": "Set up a follow-up meeting to review progress on action items.", "priority": "low", "estimated_hours": 1, "suggested_assignee": None},
            ]

        return tasks

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._generate_demo_tasks(prompt))
