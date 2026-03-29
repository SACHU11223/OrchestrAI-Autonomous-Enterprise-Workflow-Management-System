"""
OrchestrAI - Projects API Router
"""
import uuid
from fastapi import APIRouter, HTTPException, Depends
from models.schemas import ProjectCreate, ProjectUpdate
from core.security import get_current_user, require_manager
from core.database import get_db

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("")
async def list_projects(current_user: dict = Depends(get_current_user)):
    """List all projects."""
    db = get_db()
    result = db.table("projects").select("*").order("created_at", desc=True).execute()
    projects = []
    for p in result.data:
        # Get task stats
        tasks = db.table("tasks").select("*").eq("project_id", p["id"]).execute()
        task_list = tasks.data
        total = len(task_list)
        completed = sum(1 for t in task_list if t.get("status") == "completed")
        delayed = sum(1 for t in task_list if t.get("status") == "delayed")
        p["task_stats"] = {
            "total": total,
            "completed": completed,
            "in_progress": sum(1 for t in task_list if t.get("status") == "in_progress"),
            "pending": sum(1 for t in task_list if t.get("status") == "pending"),
            "delayed": delayed
        }
        # Recalculate progress
        if total > 0:
            p["progress"] = round((completed / total) * 100, 1)
        
        # Get team info
        team = db.table("teams").select("*").eq("id", p["team_id"]).execute()
        p["team_name"] = team.data[0]["name"] if team.data else "Unknown"
        projects.append(p)
    return projects


@router.post("")
async def create_project(req: ProjectCreate, current_user: dict = Depends(require_manager)):
    """Create a new project."""
    db = get_db()
    project_id = str(uuid.uuid4())
    db.table("projects").insert({
        "id": project_id,
        "name": req.name,
        "description": req.description or "",
        "team_id": req.team_id,
        "manager_id": current_user["sub"],
        "status": "planning",
        "start_date": req.start_date or "",
        "end_date": req.end_date or "",
        "progress": 0,
    }).execute()

    return {"id": project_id, "name": req.name, "message": "Project created successfully"}


@router.get("/{project_id}")
async def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    """Get project details."""
    db = get_db()
    result = db.table("projects").select("*").eq("id", project_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = result.data[0]
    tasks = db.table("tasks").select("*").eq("project_id", project_id).execute()
    project["tasks"] = tasks.data
    
    team = db.table("teams").select("*").eq("id", project["team_id"]).execute()
    project["team_name"] = team.data[0]["name"] if team.data else "Unknown"
    
    return project


@router.patch("/{project_id}")
async def update_project(project_id: str, req: ProjectUpdate, current_user: dict = Depends(require_manager)):
    """Update project details."""
    db = get_db()
    update_data = {k: v for k, v in req.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = db.table("projects").update(update_data).eq("id", project_id).execute()
    return {"message": "Project updated successfully", "data": result.data[0] if result.data else {}}
