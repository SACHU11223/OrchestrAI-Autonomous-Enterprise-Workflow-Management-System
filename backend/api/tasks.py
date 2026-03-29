"""
OrchestrAI - Tasks API Router
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from models.schemas import TaskCreate, TaskUpdate
from core.security import get_current_user, require_manager
from core.database import get_db
from core.websockets import manager
import asyncio
from services.email_service import send_email_notification

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("")
async def list_tasks(project_id: str = None, assigned_to: str = None, status: str = None, current_user: dict = Depends(get_current_user)):
    """List tasks with optional filters."""
    db = get_db()
    query = db.table("tasks").select("*")
    
    if project_id:
        query = query.eq("project_id", project_id)
    if assigned_to:
        query = query.eq("assigned_to", assigned_to)
    if status:
        query = query.eq("status", status)
    
    result = query.order("created_at", desc=True).execute()
    
    # Enrich with user info
    tasks = []
    for t in result.data:
        if t.get("assigned_to"):
            user_result = db.table("users").select("*").eq("id", t["assigned_to"]).execute()
            if user_result.data:
                u = user_result.data[0]
                t["assigned_user"] = {"id": u["id"], "full_name": u["full_name"], "designation": u.get("designation", "")}
        tasks.append(t)
    return tasks


@router.post("")
async def create_task(req: TaskCreate, current_user: dict = Depends(require_manager)):
    """Create a new task."""
    db = get_db()
    task_id = str(uuid.uuid4())
    
    db.table("tasks").insert({
        "id": task_id,
        "title": req.title,
        "description": req.description or "",
        "project_id": req.project_id,
        "assigned_to": req.assigned_to or "",
        "assigned_by": current_user["sub"],
        "status": "pending",
        "priority": req.priority.value,
        "deadline": req.deadline or "",
        "estimated_hours": req.estimated_hours or 0,
    }).execute()

    # Create notification
    if req.assigned_to:
        db.table("notifications").insert({
            "id": str(uuid.uuid4()),
            "user_id": req.assigned_to,
            "title": "📋 New Task Assigned",
            "message": f'You have been assigned: "{req.title}"',
            "notification_type": "assignment",
            "related_task_id": task_id,
            "related_project_id": req.project_id,
        }).execute()
        
    await manager.broadcast({
        "type": "NEW_TASK",
        "task_id": task_id,
        "project_id": req.project_id,
        "assigned_to": req.assigned_to
    })
    
    # Send email notification to user
    if req.assigned_to:
        user_res = db.table("users").select("email, full_name").eq("id", req.assigned_to).execute()
        if user_res.data:
            user = user_res.data[0]
            email_body = f"Hello {user['full_name']},\n\nYou have been assigned a new task: '{req.title}'.\nPriority: {req.priority.value.upper()}\nDeadline: {req.deadline or 'TBD'}\n\nPlease check your OrchestrAI dashboard."
            asyncio.create_task(send_email_notification(
                to_email=user["email"],
                subject="New Task Assignment",
                body=email_body
            ))

    return {"id": task_id, "title": req.title, "message": "Task created successfully"}


@router.patch("/{task_id}")
async def update_task(task_id: str, req: TaskUpdate, current_user: dict = Depends(get_current_user)):
    """Update a task (status, hours, etc)."""
    db = get_db()
    
    update_data = {}
    if req.status is not None:
        update_data["status"] = req.status
        if req.status == "completed":
            update_data["completed_at"] = datetime.now().isoformat()
    if req.actual_hours is not None:
        update_data["actual_hours"] = req.actual_hours
    if req.title is not None:
        update_data["title"] = req.title
    if req.description is not None:
        update_data["description"] = req.description
    if req.priority is not None:
        update_data["priority"] = req.priority
    if req.deadline is not None:
        update_data["deadline"] = req.deadline
    if req.assigned_to is not None:
        update_data["assigned_to"] = req.assigned_to

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = db.table("tasks").update(update_data).eq("id", task_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update project progress
    task = result.data[0]
    if task.get("project_id"):
        all_tasks = db.table("tasks").select("*").eq("project_id", task["project_id"]).execute()
        total = len(all_tasks.data)
        completed = sum(1 for t in all_tasks.data if t.get("status") == "completed")
        progress = round((completed / total) * 100, 1) if total > 0 else 0
        db.table("projects").update({"progress": progress}).eq("id", task["project_id"]).execute()

    await manager.broadcast({
        "type": "TASK_UPDATED",
        "task_id": task_id,
        "project_id": task.get("project_id"),
        "assigned_to": task.get("assigned_to"),
        "status": task.get("status")
    })

    return {"message": "Task updated successfully", "data": result.data[0]}


@router.get("/my")
async def my_tasks(current_user: dict = Depends(get_current_user)):
    """Get tasks assigned to current user."""
    db = get_db()
    result = db.table("tasks").select("*").eq("assigned_to", current_user["sub"]).order("created_at", desc=True).execute()
    
    tasks = []
    for t in result.data:
        # Get project name
        if t.get("project_id"):
            proj = db.table("projects").select("*").eq("id", t["project_id"]).execute()
            t["project_name"] = proj.data[0]["name"] if proj.data else "Unknown"
        tasks.append(t)
    return tasks


@router.get("/{task_id}")
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    """Get task details."""
    db = get_db()
    result = db.table("tasks").select("*").eq("id", task_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return result.data[0]
