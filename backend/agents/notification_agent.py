"""
OrchestrAI - Notification Agent
Sends email notifications for deadlines, delays, and performance alerts.
"""
import json
from agents.base_agent import BaseAgent


class NotificationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Notification Agent",
            system_instruction="""You are a Notification Agent. Generate professional
            notification messages for various workplace events."""
        )

    async def generate_notification(self, event_type: str, context: dict) -> dict:
        """Generate a notification message for a given event."""
        templates = {
            "deadline": self._deadline_notification,
            "delay": self._delay_notification,
            "assignment": self._assignment_notification,
            "performance": self._performance_notification,
            "general": self._general_notification,
        }

        generator = templates.get(event_type, self._general_notification)
        return generator(context)

    def _deadline_notification(self, ctx: dict) -> dict:
        task = ctx.get("task_title", "a task")
        deadline = ctx.get("deadline", "soon")
        return {
            "title": "⏰ Task Deadline Approaching",
            "message": f'Your task "{task}" is due on {deadline}. Please ensure it is completed on time.',
            "notification_type": "deadline",
            "priority": "high"
        }

    def _delay_notification(self, ctx: dict) -> dict:
        task = ctx.get("task_title", "a task")
        delay_days = ctx.get("delay_days", 0)
        return {
            "title": "⚠️ Task Delay Alert",
            "message": f'Your task "{task}" has been flagged as potentially delayed by {delay_days} days. Please update your status.',
            "notification_type": "delay",
            "priority": "high"
        }

    def _assignment_notification(self, ctx: dict) -> dict:
        task = ctx.get("task_title", "a new task")
        project = ctx.get("project_name", "a project")
        deadline = ctx.get("deadline", "TBD")
        return {
            "title": "📋 New Task Assigned",
            "message": f'You have been assigned "{task}" in project "{project}". Deadline: {deadline}.',
            "notification_type": "assignment",
            "priority": "medium"
        }

    def _performance_notification(self, ctx: dict) -> dict:
        score = ctx.get("score", 0)
        period = ctx.get("period", "this month")
        if score >= 90:
            return {
                "title": "🌟 Outstanding Performance!",
                "message": f"Congratulations! Your performance score for {period} is {score}%. Keep up the excellent work!",
                "notification_type": "performance",
                "priority": "low"
            }
        elif score >= 70:
            return {
                "title": "📊 Performance Update",
                "message": f"Your performance score for {period} is {score}%. Good progress! Check your dashboard for details.",
                "notification_type": "performance",
                "priority": "low"
            }
        else:
            return {
                "title": "📊 Performance Review Needed",
                "message": f"Your performance score for {period} is {score}%. Let's schedule a meeting to discuss improvement areas.",
                "notification_type": "performance",
                "priority": "medium"
            }

    def _general_notification(self, ctx: dict) -> dict:
        return {
            "title": ctx.get("title", "📬 Notification"),
            "message": ctx.get("message", "You have a new notification."),
            "notification_type": "general",
            "priority": ctx.get("priority", "low")
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps({"title": "Notification", "message": "Demo notification"})
