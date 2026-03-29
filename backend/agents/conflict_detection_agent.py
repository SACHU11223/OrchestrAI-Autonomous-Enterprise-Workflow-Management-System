"""
OrchestrAI - Conflict Detection Agent
Detects team conflicts from feedback patterns and interactions.
"""
import json
from agents.base_agent import BaseAgent


class ConflictDetectionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Conflict Detection Agent",
            system_instruction="""You are a Conflict Detection Agent. Analyze team dynamics,
            employee feedback, and interaction patterns to identify potential conflicts."""
        )

    async def detect(self, team_data: dict) -> dict:
        """Detect potential conflicts in team."""
        prompt = f"""Analyze this team data for potential conflicts:

TEAM DATA:
{json.dumps(team_data, indent=2)}

Return JSON with:
- "conflict_detected": boolean
- "conflict_level": "none" | "low" | "medium" | "high"
- "conflict_areas": [{{"area": "description", "severity": "low|medium|high", "involved_members": ["name1"]}}]
- "root_causes": ["cause1"]
- "resolution_suggestions": ["suggestion1"]"""

        result = await self._call_gemini_json(prompt)
        if result and "conflict_detected" in result:
            return result

        return self._demo_detect(team_data)

    def _demo_detect(self, team_data: dict) -> dict:
        feedback_list = team_data.get("feedback", [])
        neg_count = sum(1 for f in feedback_list if f.get("sentiment") == "negative")
        total = len(feedback_list) or 1
        neg_ratio = neg_count / total

        conflict_areas = []
        if neg_ratio > 0.3:
            conflict_areas.append({
                "area": "Workload distribution imbalance",
                "severity": "medium",
                "involved_members": ["Team members with negative feedback"]
            })
        
        delayed_tasks = [t for t in team_data.get("tasks", []) if t.get("status") == "delayed"]
        if len(delayed_tasks) > 1:
            conflict_areas.append({
                "area": "Multiple delayed tasks causing team friction",
                "severity": "medium",
                "involved_members": ["Team members with delayed tasks"]
            })

        return {
            "conflict_detected": len(conflict_areas) > 0,
            "conflict_level": "medium" if conflict_areas else "none",
            "conflict_areas": conflict_areas,
            "root_causes": ["Workload imbalance", "Resource constraints"] if conflict_areas else [],
            "resolution_suggestions": [
                "Hold a team retrospective to address concerns",
                "Redistribute workload more evenly",
                "Provide additional resources for blocked items"
            ] if conflict_areas else ["Team dynamics appear healthy"]
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_detect({}))
