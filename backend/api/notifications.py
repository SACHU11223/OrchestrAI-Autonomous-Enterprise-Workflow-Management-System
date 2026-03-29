"""
OrchestrAI - Notifications API Router
"""
import uuid
from fastapi import APIRouter, Depends
from core.security import get_current_user
from core.database import get_db
from services.email_service import send_email_notification

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("")
async def list_notifications(current_user: dict = Depends(get_current_user)):
    """Get notifications for current user."""
    db = get_db()
    result = db.table("notifications").select("*").eq("user_id", current_user["sub"]).order("created_at", desc=True).execute()
    return result.data


@router.patch("/{notification_id}/read")
async def mark_read(notification_id: str, current_user: dict = Depends(get_current_user)):
    """Mark a notification as read."""
    db = get_db()
    db.table("notifications").update({"is_read": 1}).eq("id", notification_id).execute()
    return {"message": "Notification marked as read"}


@router.post("/mark-all-read")
async def mark_all_read(current_user: dict = Depends(get_current_user)):
    """Mark all notifications as read."""
    db = get_db()
    db.table("notifications").update({"is_read": 1}).eq("user_id", current_user["sub"]).execute()
    return {"message": "All notifications marked as read"}


@router.post("/send-email/{notification_id}")
async def send_notification_email(notification_id: str, current_user: dict = Depends(get_current_user)):
    """Send notification via email."""
    db = get_db()
    notif = db.table("notifications").select("*").eq("id", notification_id).execute()
    if not notif.data:
        return {"error": "Notification not found"}
    
    n = notif.data[0]
    user = db.table("users").select("*").eq("id", n["user_id"]).execute()
    if not user.data:
        return {"error": "User not found"}

    success = await send_email_notification(
        to_email=user.data[0]["email"],
        subject=n["title"],
        body=n["message"],
    )

    if success:
        db.table("notifications").update({"is_email_sent": 1}).eq("id", notification_id).execute()

    return {"message": "Email sent" if success else "Email sending configured but not active in demo mode"}
