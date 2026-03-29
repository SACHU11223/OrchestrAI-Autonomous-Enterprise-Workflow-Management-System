"""
OrchestrAI - Teams API Router
"""
import uuid
from fastapi import APIRouter, HTTPException, Depends
from models.schemas import TeamCreate, TeamResponse, AddMemberRequest
from core.security import get_current_user, require_manager
from core.database import get_db

router = APIRouter(prefix="/api/teams", tags=["Teams"])


@router.get("")
async def list_teams(current_user: dict = Depends(get_current_user)):
    """List all teams."""
    db = get_db()
    result = db.table("teams").select("*").execute()
    teams = []
    for team in result.data:
        members_result = db.table("team_members").select("*").eq("team_id", team["id"]).execute()
        member_details = []
        for m in members_result.data:
            user_result = db.table("users").select("*").eq("id", m["user_id"]).execute()
            if user_result.data:
                u = user_result.data[0]
                u.pop("password_hash", None)
                member_details.append(u)
        team["members"] = member_details
        team["member_count"] = len(member_details)
        teams.append(team)
    return teams


@router.post("")
async def create_team(req: TeamCreate, current_user: dict = Depends(require_manager)):
    """Create a new team."""
    db = get_db()
    team_id = str(uuid.uuid4())
    db.table("teams").insert({
        "id": team_id,
        "name": req.name,
        "description": req.description or "",
        "manager_id": current_user["sub"],
        "color": req.color or "#667eea",
    }).execute()

    return {"id": team_id, "name": req.name, "message": "Team created successfully"}


@router.post("/{team_id}/members")
async def add_member(team_id: str, req: AddMemberRequest, current_user: dict = Depends(require_manager)):
    """Add a member to a team."""
    db = get_db()
    # Verify team exists
    team = db.table("teams").select("*").eq("id", team_id).execute()
    if not team.data:
        raise HTTPException(status_code=404, detail="Team not found")

    # Check if already a member
    existing = db.table("team_members").select("*").eq("team_id", team_id).eq("user_id", req.user_id).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="User is already a team member")

    db.table("team_members").insert({
        "id": str(uuid.uuid4()),
        "team_id": team_id,
        "user_id": req.user_id,
    }).execute()

    return {"message": "Member added successfully"}


@router.delete("/{team_id}/members/{user_id}")
async def remove_member(team_id: str, user_id: str, current_user: dict = Depends(require_manager)):
    """Remove a member from a team."""
    db = get_db()
    db.table("team_members").delete().eq("team_id", team_id).eq("user_id", user_id).execute()
    return {"message": "Member removed successfully"}


@router.get("/{team_id}")
async def get_team(team_id: str, current_user: dict = Depends(get_current_user)):
    """Get team details with members."""
    db = get_db()
    result = db.table("teams").select("*").eq("id", team_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Team not found")

    team = result.data[0]
    members_result = db.table("team_members").select("*").eq("team_id", team_id).execute()
    member_details = []
    for m in members_result.data:
        user_result = db.table("users").select("*").eq("id", m["user_id"]).execute()
        if user_result.data:
            u = user_result.data[0]
            u.pop("password_hash", None)
            member_details.append(u)
    team["members"] = member_details
    team["member_count"] = len(member_details)
    return team
