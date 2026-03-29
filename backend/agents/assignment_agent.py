"""
OrchestrAI - Assignment Agent
Assigns tasks to team members based on skills, workload, and availability.
"""
import json
import random
from agents.base_agent import BaseAgent


class AssignmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Assignment Agent",
            system_instruction="""You are a Task Assignment Agent. Your job is to optimally assign tasks
            to team members based on their skills, current workload, expertise, and availability.
            Consider load balancing and skill matching when making assignments."""
        )

    async def assign(self, tasks: list, team_members: list) -> list:
        """Assign tasks to team members."""
        if not team_members:
            return tasks

        prompt = f"""Assign these tasks to the most suitable team members.

TASKS:
{json.dumps(tasks, indent=2)}

TEAM MEMBERS:
{json.dumps(team_members, indent=2)}

For each task, set the "assigned_to_id" and "assigned_to_name" fields based on the best match.
Consider skills, workload balance, and expertise.
Return the updated tasks array as JSON."""

        result = await self._call_gemini_json(prompt)
        if isinstance(result, list) and len(result) > 0:
            return result
        
        # Fallback: round-robin assignment
        return self._demo_assign(tasks, team_members)

    def _demo_assign(self, tasks: list, team_members: list) -> list:
        """Demo assignment using round-robin with some intelligence."""
        for i, task in enumerate(tasks):
            if task.get("suggested_assignee"):
                # Try to match by name
                for member in team_members:
                    name = member.get("full_name", member.get("name", ""))
                    if task["suggested_assignee"].lower() in name.lower():
                        task["assigned_to_id"] = member.get("id", "")
                        task["assigned_to_name"] = name
                        break
            
            if "assigned_to_id" not in task:
                # Round-robin
                member = team_members[i % len(team_members)]
                task["assigned_to_id"] = member.get("id", "")
                task["assigned_to_name"] = member.get("full_name", member.get("name", ""))
        
        return tasks

    def _fallback_response(self, prompt: str) -> str:
        return '[]'
