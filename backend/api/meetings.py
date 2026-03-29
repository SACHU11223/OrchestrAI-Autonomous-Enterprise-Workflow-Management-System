"""
OrchestrAI - Meetings API Router
Handles meeting input and AI-powered summarization/task extraction.
"""
import uuid
import json
from fastapi import APIRouter, HTTPException, Depends
from models.schemas import MeetingCreate, MeetingResponse
from core.security import get_current_user, require_manager
from core.database import get_db
from agents.orchestrator import get_orchestrator
import asyncio
from services.email_service import send_email_notification
from core.websockets import manager

router = APIRouter(prefix="/api/meetings", tags=["Meetings"])


@router.get("")
async def list_meetings(current_user: dict = Depends(get_current_user)):
    """List all meetings."""
    db = get_db()
    result = db.table("meetings").select("*").order("created_at", desc=True).execute()
    return result.data


@router.post("")
async def create_meeting(req: MeetingCreate, current_user: dict = Depends(require_manager)):
    """Create a meeting and process with AI agents."""
    db = get_db()
    orchestrator = get_orchestrator()

    # Get team members if team_id provided
    team_members = []
    if req.team_id:
        members_result = db.table("team_members").select("*").eq("team_id", req.team_id).execute()
        for m in members_result.data:
            user_result = db.table("users").select("*").eq("id", m["user_id"]).execute()
            if user_result.data:
                u = user_result.data[0]
                team_members.append({
                    "id": u["id"],
                    "full_name": u["full_name"],
                    "designation": u.get("designation", ""),
                    "department": u.get("department", ""),
                })

    # Get project name
    project_name = ""
    if req.project_id:
        proj = db.table("projects").select("*").eq("id", req.project_id).execute()
        if proj.data:
            project_name = proj.data[0]["name"]

    # Process meeting through AI orchestrator
    ai_result = await orchestrator.process_meeting(
        transcript=req.transcript,
        project_name=project_name,
        team_members=team_members,
    )

    meeting_id = str(uuid.uuid4())
    
    # Store meeting
    db.table("meetings").insert({
        "id": meeting_id,
        "title": req.title,
        "project_id": req.project_id or "",
        "team_id": req.team_id or "",
        "conducted_by": current_user["sub"],
        "transcript": req.transcript,
        "summary": ai_result["summary"],
        "action_items": json.dumps(ai_result.get("tasks", [])),
        "extracted_tasks": json.dumps(ai_result.get("tasks", [])),
        "duration_minutes": req.duration_minutes or 0,
    }).execute()

    # Create tasks from AI extraction
    created_tasks = []
    for task_data in ai_result.get("tasks", []):
        task_id = str(uuid.uuid4())
        assigned_to = task_data.get("assigned_to_id", "")
        
        db.table("tasks").insert({
            "id": task_id,
            "title": task_data.get("title", "Untitled Task"),
            "description": task_data.get("description", ""),
            "project_id": req.project_id or "",
            "assigned_to": assigned_to,
            "assigned_by": current_user["sub"],
            "status": "pending",
            "priority": task_data.get("priority", "medium"),
            "deadline": task_data.get("deadline", ""),
            "estimated_hours": task_data.get("estimated_hours", 8),
            "meeting_id": meeting_id,
        }).execute()

        # Create notification for assigned user
        if assigned_to:
            db.table("notifications").insert({
                "id": str(uuid.uuid4()),
                "user_id": assigned_to,
                "title": "📋 New Task Assigned",
                "message": f'You have been assigned "{task_data.get("title", "a task")}" from meeting "{req.title}".',
                "notification_type": "assignment",
                "related_task_id": task_id,
                "related_project_id": req.project_id or "",
            }).execute()
            
            # Broadcast WebSocket
            asyncio.create_task(manager.broadcast({
                "type": "NEW_TASK",
                "task_id": task_id,
                "project_id": req.project_id or "",
                "assigned_to": assigned_to
            }))
            
            # Send Email
            user_res = db.table("users").select("email, full_name").eq("id", assigned_to).execute()
            if user_res.data:
                u = user_res.data[0]
                asyncio.create_task(send_email_notification(
                    to_email=u["email"],
                    subject=f"New Task Assigned via Meeting: {req.title}",
                    body=f"Hello {u['full_name']},\n\nDuring the meeting '{req.title}', an AI generated task was assigned to you: '{task_data.get('title')}'\n\nDeadline: {task_data.get('deadline', 'TBD')}\nPriority: {task_data.get('priority', 'medium').upper()}\n\nCheck your dashboard for details."
                ))

        created_tasks.append({
            "id": task_id,
            "title": task_data.get("title"),
            "assigned_to": task_data.get("assigned_to_name", ""),
            "priority": task_data.get("priority", "medium"),
            "deadline": task_data.get("deadline", ""),
        })

    return {
        "meeting_id": meeting_id,
        "summary": ai_result["summary"],
        "tasks_created": len(created_tasks),
        "tasks": created_tasks,
        "message": f"Meeting processed successfully. {len(created_tasks)} tasks created."
    }


@router.get("/{meeting_id}")
async def get_meeting(meeting_id: str, current_user: dict = Depends(get_current_user)):
    """Get meeting details."""
    db = get_db()
    result = db.table("meetings").select("*").eq("id", meeting_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = result.data[0]
    # Parse JSON fields
    for field in ["action_items", "extracted_tasks"]:
        if isinstance(meeting.get(field), str):
            try:
                meeting[field] = json.loads(meeting[field])
            except:
                meeting[field] = []
    return meeting
