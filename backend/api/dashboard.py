"""
OrchestrAI - Dashboard API Router
Aggregated dashboard data for managers and employees.
"""
import json
from fastapi import APIRouter, Depends
from core.security import get_current_user
from core.database import get_db
from agents.orchestrator import get_orchestrator

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/manager")
async def manager_dashboard(current_user: dict = Depends(get_current_user)):
    """Get aggregated manager dashboard data."""
    db = get_db()

    # Tasks overview
    all_tasks = db.table("tasks").select("*").execute()
    tasks = all_tasks.data
    
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    pending = sum(1 for t in tasks if t.get("status") == "pending")
    in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
    delayed = sum(1 for t in tasks if t.get("status") == "delayed")
    total = len(tasks)

    # Projects
    projects = db.table("projects").select("*").execute()
    active_projects = sum(1 for p in projects.data if p.get("status") == "active")

    # Teams
    teams = db.table("teams").select("*").execute()

    # Employees
    employees = db.table("users").select("*").eq("role", "employee").execute()

    # Performance data
    perf = db.table("performance").select("*").execute()
    avg_performance = 0
    avg_productivity = 0
    if perf.data:
        avg_performance = sum(p.get("performance_score", 0) for p in perf.data) / len(perf.data)
        avg_productivity = sum(p.get("productivity_score", 0) for p in perf.data) / len(perf.data)

    # Notifications
    notifs = db.table("notifications").select("*").eq("user_id", current_user["sub"]).eq("is_read", 0).execute()

    # Feedback sentiment distribution
    feedback = db.table("feedback").select("*").execute()
    sentiment_dist = {"positive": 0, "neutral": 0, "negative": 0}
    for f in feedback.data:
        s = f.get("sentiment", "neutral")
        if s in sentiment_dist:
            sentiment_dist[s] += 1

    # Task trend (by priority)
    priority_dist = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for t in tasks:
        p = t.get("priority", "medium")
        if p in priority_dist:
            priority_dist[p] += 1

    # Project progress
    project_progress = []
    for p in projects.data:
        project_progress.append({
            "name": p["name"],
            "progress": p.get("progress", 0),
            "status": p.get("status", "planning"),
        })

    # Employee performance list
    employee_performance = []
    for emp in employees.data:
        emp_perf = [p for p in perf.data if p.get("user_id") == emp["id"]]
        score = emp_perf[0].get("performance_score", 0) if emp_perf else 0
        prod = emp_perf[0].get("productivity_score", 0) if emp_perf else 0
        emp_tasks = [t for t in tasks if t.get("assigned_to") == emp["id"]]
        emp_completed = sum(1 for t in emp_tasks if t.get("status") == "completed")
        
        employee_performance.append({
            "id": emp["id"],
            "name": emp["full_name"],
            "department": emp.get("department", ""),
            "performance_score": score,
            "productivity_score": prod,
            "tasks_completed": emp_completed,
            "tasks_total": len(emp_tasks),
        })

    # Delay alerts
    delay_alerts = [t for t in tasks if t.get("delay_probability", 0) > 0.5 and t.get("status") != "completed"]

    return {
        "stats": {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "in_progress_tasks": in_progress,
            "delayed_tasks": delayed,
            "total_projects": len(projects.data),
            "active_projects": active_projects,
            "total_teams": len(teams.data),
            "total_employees": len(employees.data),
            "average_performance": round(avg_performance, 1),
            "average_productivity": round(avg_productivity, 1),
            "completion_rate": round((completed / total * 100), 1) if total > 0 else 0,
            "delay_rate": round((delayed / total * 100), 1) if total > 0 else 0,
            "unread_notifications": len(notifs.data),
        },
        "charts": {
            "task_status": {"completed": completed, "pending": pending, "in_progress": in_progress, "delayed": delayed},
            "task_priority": priority_dist,
            "sentiment_distribution": sentiment_dist,
            "project_progress": project_progress,
        },
        "employee_performance": sorted(employee_performance, key=lambda x: x["performance_score"], reverse=True),
        "delay_alerts": delay_alerts[:5],
        "recent_feedback": feedback.data[:5],
    }


@router.get("/employee")
async def employee_dashboard(current_user: dict = Depends(get_current_user)):
    """Get employee-specific dashboard data."""
    db = get_db()
    user_id = current_user["sub"]

    # My tasks
    my_tasks = db.table("tasks").select("*").eq("assigned_to", user_id).execute()
    tasks = my_tasks.data
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    pending = sum(1 for t in tasks if t.get("status") == "pending")
    in_progress = sum(1 for t in tasks if t.get("status") == "in_progress")
    delayed = sum(1 for t in tasks if t.get("status") == "delayed")

    # My performance
    perf = db.table("performance").select("*").eq("user_id", user_id).execute()
    performance = perf.data[0] if perf.data else {}

    # My feedback
    feedback = db.table("feedback").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()

    # My notifications
    notifs = db.table("notifications").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    unread = sum(1 for n in notifs.data if not n.get("is_read"))

    # Sentiment trend
    sentiment_scores = [f.get("sentiment_score", 0.5) for f in feedback.data[:10]]

    # Enrich tasks with project names
    for t in tasks:
        if t.get("project_id"):
            proj = db.table("projects").select("*").eq("id", t["project_id"]).execute()
            t["project_name"] = proj.data[0]["name"] if proj.data else "Unknown"

    return {
        "stats": {
            "total_tasks": len(tasks),
            "completed_tasks": completed,
            "pending_tasks": pending,
            "in_progress_tasks": in_progress,
            "delayed_tasks": delayed,
            "completion_rate": round((completed / len(tasks) * 100), 1) if tasks else 0,
            "performance_score": performance.get("performance_score", 0),
            "productivity_score": performance.get("productivity_score", 0),
            "unread_notifications": unread,
        },
        "tasks": tasks,
        "performance": performance,
        "recent_feedback": feedback.data[:5],
        "notifications": notifs.data[:10],
        "sentiment_trend": sentiment_scores,
    }


@router.get("/analytics")
async def analytics_dashboard(current_user: dict = Depends(get_current_user)):
    """Get analytics data for charts and reports."""
    db = get_db()
    orchestrator = get_orchestrator()

    # All data
    tasks = db.table("tasks").select("*").execute()
    projects = db.table("projects").select("*").execute()
    feedback = db.table("feedback").select("*").execute()
    performance = db.table("performance").select("*").execute()
    teams = db.table("teams").select("*").execute()

    # Team-wise task distribution
    team_tasks = {}
    for team in teams.data:
        team_projects = [p for p in projects.data if p.get("team_id") == team["id"]]
        project_ids = [p["id"] for p in team_projects]
        team_task_list = [t for t in tasks.data if t.get("project_id") in project_ids]
        team_tasks[team["name"]] = {
            "total": len(team_task_list),
            "completed": sum(1 for t in team_task_list if t.get("status") == "completed"),
            "delayed": sum(1 for t in team_task_list if t.get("status") == "delayed"),
        }

    # Team performance analysis
    team_analysis = {}
    for team in teams.data:
        members = db.table("team_members").select("*").eq("team_id", team["id"]).execute()
        member_ids = [m["user_id"] for m in members.data]
        team_perf = [p for p in performance.data if p.get("user_id") in member_ids]
        avg_score = sum(p.get("performance_score", 0) for p in team_perf) / len(team_perf) if team_perf else 0
        
        team_analysis[team["name"]] = {
            "avg_performance": round(avg_score, 1),
            "member_count": len(member_ids),
            "color": team.get("color", "#667eea"),
        }

    # Risk analysis per project
    project_risks = []
    for p in projects.data:
        proj_tasks = [t for t in tasks.data if t.get("project_id") == p["id"]]
        delayed_count = sum(1 for t in proj_tasks if t.get("status") == "delayed")
        total = len(proj_tasks) or 1
        risk_score = min(100, (delayed_count / total) * 100 + p.get("risk_score", 0))
        project_risks.append({
            "name": p["name"],
            "risk_score": round(risk_score, 1),
            "progress": p.get("progress", 0),
        })

    return {
        "team_tasks": team_tasks,
        "team_performance": team_analysis,
        "project_risks": project_risks,
        "total_metrics": {
            "total_tasks": len(tasks.data),
            "total_completed": sum(1 for t in tasks.data if t.get("status") == "completed"),
            "total_feedback": len(feedback.data),
            "avg_sentiment": round(sum(f.get("sentiment_score", 0.5) for f in feedback.data) / max(len(feedback.data), 1), 2),
        },
    }
