"""
OrchestrAI - AI Orchestrator
Central controller that coordinates all AI agents.
"""
import json
from typing import Optional
from agents.meeting_agent import MeetingAgent
from agents.task_extraction_agent import TaskExtractionAgent
from agents.assignment_agent import AssignmentAgent
from agents.deadline_agent import DeadlineAgent
from agents.feedback_agent import FeedbackAgent
from agents.sentiment_agent import SentimentAgent
from agents.delay_prediction_agent import DelayPredictionAgent
from agents.conflict_detection_agent import ConflictDetectionAgent
from agents.performance_agent import PerformanceAgent
from agents.report_agent import ReportAgent
from agents.notification_agent import NotificationAgent
from agents.workload_balancer_agent import WorkloadBalancerAgent
from agents.risk_prediction_agent import RiskPredictionAgent
from agents.productivity_agent import ProductivityAgent


class Orchestrator:
    """AI Orchestrator that coordinates all specialized agents."""

    def __init__(self):
        self.meeting_agent = MeetingAgent()
        self.task_extraction_agent = TaskExtractionAgent()
        self.assignment_agent = AssignmentAgent()
        self.deadline_agent = DeadlineAgent()
        self.feedback_agent = FeedbackAgent()
        self.sentiment_agent = SentimentAgent()
        self.delay_prediction_agent = DelayPredictionAgent()
        self.conflict_detection_agent = ConflictDetectionAgent()
        self.performance_agent = PerformanceAgent()
        self.report_agent = ReportAgent()
        self.notification_agent = NotificationAgent()
        self.workload_balancer_agent = WorkloadBalancerAgent()
        self.risk_prediction_agent = RiskPredictionAgent()
        self.productivity_agent = ProductivityAgent()

    async def process_meeting(self, transcript: str, project_name: str = "", team_members: list = None):
        """Full meeting processing pipeline: summarize → extract tasks → assign → set deadlines."""
        # Step 1: Summarize meeting
        summary = await self.meeting_agent.summarize(transcript)

        # Step 2: Extract tasks
        tasks = await self.task_extraction_agent.extract(transcript, summary)

        # Step 3: Assign tasks to team members
        if team_members:
            tasks = await self.assignment_agent.assign(tasks, team_members)

        # Step 4: Set deadlines
        tasks = await self.deadline_agent.set_deadlines(tasks, project_name)

        return {
            "summary": summary,
            "tasks": tasks,
            "task_count": len(tasks),
        }

    async def process_feedback(self, feedback_text: str, employee_name: str = "", task_title: str = ""):
        """Feedback processing pipeline: analyze sentiment → predict delays."""
        # Step 1: Sentiment analysis
        sentiment = await self.sentiment_agent.analyze(feedback_text, employee_name)

        # Step 2: Delay prediction
        delay_prediction = await self.delay_prediction_agent.predict(
            feedback_text, task_title, sentiment
        )

        # Step 3: Feedback analysis
        analysis = await self.feedback_agent.analyze(
            feedback_text, employee_name, sentiment
        )

        return {
            "sentiment": sentiment,
            "delay_prediction": delay_prediction,
            "analysis": analysis,
        }

    async def analyze_team(self, team_data: dict):
        """Team analysis pipeline: conflicts → workload → risk."""
        # Step 1: Conflict detection
        conflicts = await self.conflict_detection_agent.detect(team_data)

        # Step 2: Workload balancing
        workload = await self.workload_balancer_agent.analyze(team_data)

        # Step 3: Risk prediction
        risks = await self.risk_prediction_agent.predict(team_data)

        return {
            "conflicts": conflicts,
            "workload_recommendations": workload,
            "risks": risks,
        }

    async def calculate_performance(self, employee_data: dict):
        """Performance calculation pipeline."""
        # Step 1: Performance score
        performance = await self.performance_agent.calculate(employee_data)

        # Step 2: Productivity score
        productivity = await self.productivity_agent.calculate(employee_data)

        return {
            "performance": performance,
            "productivity": productivity,
        }

    async def generate_report(self, report_data: dict, report_type: str = "weekly"):
        """Report generation pipeline."""
        report = await self.report_agent.generate(report_data, report_type)
        return report


# Singleton orchestrator instance
_orchestrator: Optional[Orchestrator] = None


def get_orchestrator() -> Orchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator
