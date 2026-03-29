"""
OrchestrAI - Workload Balancer Agent
Distributes work evenly across team members.
"""
import json
from agents.base_agent import BaseAgent


class WorkloadBalancerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Workload Balancer Agent",
            system_instruction="""You are a Workload Balancing Agent. Analyze task distribution
            across team members and recommend rebalancing for optimal productivity."""
        )

    async def analyze(self, team_data: dict) -> dict:
        """Analyze workload distribution and suggest rebalancing."""
        prompt = f"""Analyze the workload distribution:

TEAM DATA:
{json.dumps(team_data, indent=2)}

Return JSON with:
- "is_balanced": boolean
- "balance_score": float 0-100
- "member_workloads": [{{"name": "member", "current_tasks": int, "estimated_hours": float, "load_level": "low|medium|high|overloaded"}}]
- "recommendations": ["rec1"]
- "suggested_transfers": [{{"task": "task name", "from": "member1", "to": "member2", "reason": "reason"}}] or []"""

        result = await self._call_gemini_json(prompt)
        if result and "is_balanced" in result:
            return result

        return self._demo_balance(team_data)

    def _demo_balance(self, team_data: dict) -> dict:
        members = team_data.get("members", [])
        tasks = team_data.get("tasks", [])

        member_loads = []
        for m in members:
            mid = m.get("id", "")
            name = m.get("full_name", m.get("name", "Unknown"))
            user_tasks = [t for t in tasks if t.get("assigned_to") == mid and t.get("status") != "completed"]
            hours = sum(t.get("estimated_hours", 8) for t in user_tasks)
            count = len(user_tasks)
            
            if hours > 40:
                level = "overloaded"
            elif hours > 25:
                level = "high"
            elif hours > 10:
                level = "medium"
            else:
                level = "low"

            member_loads.append({
                "name": name,
                "current_tasks": count,
                "estimated_hours": hours,
                "load_level": level
            })

        overloaded = [m for m in member_loads if m["load_level"] in ("overloaded", "high")]
        underloaded = [m for m in member_loads if m["load_level"] == "low"]
        is_balanced = len(overloaded) == 0

        suggestions = []
        if overloaded and underloaded:
            suggestions.append({
                "task": "Consider transferring tasks",
                "from": overloaded[0]["name"],
                "to": underloaded[0]["name"],
                "reason": f"{overloaded[0]['name']} has {overloaded[0]['estimated_hours']}h while {underloaded[0]['name']} has {underloaded[0]['estimated_hours']}h"
            })

        hours_list = [m["estimated_hours"] for m in member_loads] if member_loads else [0]
        avg_hours = sum(hours_list) / len(hours_list) if hours_list else 0
        max_dev = max(abs(h - avg_hours) for h in hours_list) if hours_list else 0
        balance_score = max(0, 100 - (max_dev / max(avg_hours, 1)) * 100)

        return {
            "is_balanced": is_balanced,
            "balance_score": round(balance_score, 1),
            "member_workloads": member_loads,
            "recommendations": [
                f"{'Workload is well-balanced.' if is_balanced else 'Redistribute tasks from overloaded members.'}",
                f"Average team load: {avg_hours:.0f} hours per member."
            ],
            "suggested_transfers": suggestions
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_balance({}))
