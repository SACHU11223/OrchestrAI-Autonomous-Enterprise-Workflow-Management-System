"""
OrchestrAI - Feedback API Router
Handles daily employee feedback with AI sentiment analysis.
"""
import uuid
import json
from fastapi import APIRouter, HTTPException, Depends
from models.schemas import FeedbackCreate
from core.security import get_current_user
from core.database import get_db
from agents.orchestrator import get_orchestrator
import asyncio
from services.email_service import send_email_notification

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


@router.get("")
async def list_feedback(project_id: str = None, user_id: str = None, current_user: dict = Depends(get_current_user)):
    """List feedback entries."""
    db = get_db()
    query = db.table("feedback").select("*")
    
    if project_id:
        query = query.eq("project_id", project_id)
    if user_id:
        query = query.eq("user_id", user_id)
    
    result = query.order("created_at", desc=True).execute()
    
    # Enrich with user info
    feedback_list = []
    for f in result.data:
        user_result = db.table("users").select("*").eq("id", f["user_id"]).execute()
        if user_result.data:
            u = user_result.data[0]
            f["user"] = {"id": u["id"], "full_name": u["full_name"], "designation": u.get("designation", "")}
        
        # Parse JSON fields
        if isinstance(f.get("sentiment_details"), str):
            try:
                f["sentiment_details"] = json.loads(f["sentiment_details"])
            except:
                f["sentiment_details"] = {}
        
        feedback_list.append(f)
    
    return feedback_list


@router.post("")
async def submit_feedback(req: FeedbackCreate, current_user: dict = Depends(get_current_user)):
    """Submit daily feedback with AI analysis."""
    db = get_db()
    orchestrator = get_orchestrator()

    # Get task title if available
    task_title = ""
    if req.task_id:
        task_result = db.table("tasks").select("*").eq("id", req.task_id).execute()
        if task_result.data:
            task_title = task_result.data[0].get("title", "")

    # Process feedback through AI
    ai_result = await orchestrator.process_feedback(
        feedback_text=req.content,
        employee_name=current_user.get("full_name", ""),
        task_title=task_title,
    )

    sentiment_data = ai_result.get("sentiment", {})
    delay_data = ai_result.get("delay_prediction", {})

    feedback_id = str(uuid.uuid4())
    db.table("feedback").insert({
        "id": feedback_id,
        "user_id": current_user["sub"],
        "task_id": req.task_id or None,
        "project_id": req.project_id or None,
        "content": req.content,
        "sentiment": sentiment_data.get("sentiment", "neutral"),
        "sentiment_score": sentiment_data.get("score", 0.5),
        "sentiment_details": json.dumps(sentiment_data),
        "ai_analysis": json.dumps(ai_result.get("analysis", {})),
    }).execute()

    # Update task delay probability if applicable
    if req.task_id and delay_data.get("delay_probability", 0) > 0.5:
        db.table("tasks").update({
            "delay_probability": delay_data["delay_probability"]
        }).eq("id", req.task_id).execute()
        
        # Create delay alert notification for manager
        if delay_data.get("risk_level") in ("high", "critical"):
            # Find manager
            if req.project_id:
                proj = db.table("projects").select("*").eq("id", req.project_id).execute()
                if proj.data:
                    db.table("notifications").insert({
                        "id": str(uuid.uuid4()),
                        "user_id": proj.data[0]["manager_id"],
                        "title": "⚠️ Delay Risk Detected",
                        "message": f'Task "{task_title}" has a {delay_data["delay_probability"]*100:.0f}% delay probability. Employee sentiment: {sentiment_data.get("sentiment", "unknown")}.',
                        "notification_type": "delay",
                        "related_task_id": req.task_id,
                        "related_project_id": req.project_id or "",
                    }).execute()
                    
                    # Send Email to Manager
                    if proj.data[0].get("manager_id"):
                        mgr_res = db.table("users").select("email").eq("id", proj.data[0]["manager_id"]).execute()
                        if mgr_res.data:
                            asyncio.create_task(send_email_notification(
                                to_email=mgr_res.data[0]["email"],
                                subject=f"Delay Risk Warning: {task_title}",
                                body=f"OrchestrAI detected a high risk of delay on task '{task_title}'.\n\nProbability: {delay_data['delay_probability']*100:.0f}%\nEmployee Sentiment: {sentiment_data.get('sentiment', 'unknown')}\n\nPlease review your dashboard immediately."
                            ))

    return {
        "id": feedback_id,
        "sentiment": sentiment_data,
        "delay_prediction": delay_data,
        "analysis": ai_result.get("analysis", {}),
        "message": "Feedback submitted and analyzed successfully"
    }


@router.get("/analysis/{project_id}")
async def get_project_feedback_analysis(project_id: str, current_user: dict = Depends(get_current_user)):
    """Get aggregated feedback analysis for a project."""
    db = get_db()
    feedback_result = db.table("feedback").select("*").eq("project_id", project_id).execute()
    
    total = len(feedback_result.data)
    if total == 0:
        return {"total": 0, "sentiment_distribution": {}, "average_score": 0}
    
    positive = sum(1 for f in feedback_result.data if f.get("sentiment") == "positive")
    neutral = sum(1 for f in feedback_result.data if f.get("sentiment") == "neutral")
    negative = sum(1 for f in feedback_result.data if f.get("sentiment") == "negative")
    avg_score = sum(f.get("sentiment_score", 0.5) for f in feedback_result.data) / total

    return {
        "total": total,
        "sentiment_distribution": {
            "positive": positive,
            "neutral": neutral,
            "negative": negative,
        },
        "average_score": round(avg_score, 2),
        "positive_rate": round((positive / total) * 100, 1),
        "team_morale": "Good" if avg_score > 0.6 else ("Fair" if avg_score > 0.4 else "Needs Attention"),
    }
