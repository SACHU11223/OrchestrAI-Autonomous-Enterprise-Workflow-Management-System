"""
OrchestrAI - Auth API Router
Handles user registration, login, and authentication.
"""
import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from models.schemas import LoginRequest, RegisterRequest, AuthResponse, UserResponse
from core.security import hash_password, verify_password, create_access_token, get_current_user
from core.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse)
async def register(req: RegisterRequest):
    """Register a new user."""
    db = get_db()
    
    # Check if user exists
    existing = db.table("users").select("*").eq("email", req.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())
    pw_hash = hash_password(req.password)

    db.table("users").insert({
        "id": user_id,
        "email": req.email,
        "password_hash": pw_hash,
        "full_name": req.full_name,
        "role": req.role.value,
        "department": req.department or "",
        "designation": req.designation or "",
    }).execute()

    token = create_access_token({
        "sub": user_id,
        "email": req.email,
        "role": req.role.value,
        "full_name": req.full_name,
    })

    return AuthResponse(
        access_token=token,
        user={
            "id": user_id,
            "email": req.email,
            "full_name": req.full_name,
            "role": req.role.value,
            "department": req.department,
            "designation": req.designation,
        }
    )


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest):
    """Login with email and password."""
    db = get_db()
    result = db.table("users").select("*").eq("email", req.email).execute()
    
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = result.data[0]
    
    if not verify_password(req.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"],
        "full_name": user["full_name"],
    })

    return AuthResponse(
        access_token=token,
        user={
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "department": user.get("department"),
            "designation": user.get("designation"),
        }
    )


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile."""
    db = get_db()
    result = db.table("users").select("*").eq("id", current_user["sub"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    user = result.data[0]
    user.pop("password_hash", None)
    return user


@router.put("/profile")
async def update_profile(req: dict, current_user: dict = Depends(get_current_user)):
    """Update current user profile."""
    db = get_db()
    
    update_data = {}
    valid_fields = ["full_name", "department", "designation", "phone", "avatar_url"]
    
    for field in valid_fields:
        if field in req:
            update_data[field] = req[field]
            
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
        
    result = db.table("users").update(update_data).eq("id", current_user["sub"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")
        
    user = result.data[0]
    user.pop("password_hash", None)
    return {"message": "Profile updated successfully", "user": user}


@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_user)):
    """List all users (for team assignment)."""
    db = get_db()
    result = db.table("users").select("*").execute()
    users = []
    for u in result.data:
        u.pop("password_hash", None)
        users.append(u)
    return users
