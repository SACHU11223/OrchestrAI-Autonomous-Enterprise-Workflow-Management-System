"""
OrchestrAI Pydantic Models
Request/Response schemas for all API endpoints.
"""
from datetime import datetime, date
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


# ============================================================
# ENUMS
# ============================================================
class UserRole(str, Enum):
    MANAGER = "manager"
    EMPLOYEE = "employee"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class ReportType(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class NotificationType(str, Enum):
    DEADLINE = "deadline"
    DELAY = "delay"
    PERFORMANCE = "performance"
    ASSIGNMENT = "assignment"
    GENERAL = "general"


# ============================================================
# AUTH SCHEMAS
# ============================================================
class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    department: Optional[str] = None
    designation: Optional[str] = None


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# ============================================================
# USER SCHEMAS
# ============================================================
class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    avatar_url: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


# ============================================================
# TEAM SCHEMAS
# ============================================================
class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = "#667eea"


class TeamResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    manager_id: str
    color: Optional[str] = "#667eea"
    icon: Optional[str] = "users"
    created_at: Optional[str] = None
    members: Optional[List[dict]] = []
    member_count: Optional[int] = 0


class AddMemberRequest(BaseModel):
    user_id: str


# ============================================================
# PROJECT SCHEMAS
# ============================================================
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    team_id: str
    manager_id: str
    status: str = "planning"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    progress: Optional[float] = 0
    risk_score: Optional[float] = 0
    created_at: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[float] = None


# ============================================================
# TASK SCHEMAS
# ============================================================
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: str
    assigned_to: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    deadline: Optional[str] = None
    estimated_hours: Optional[float] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    project_id: str
    assigned_to: Optional[str] = None
    assigned_by: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    deadline: Optional[str] = None
    completed_at: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    delay_probability: Optional[float] = 0
    created_at: Optional[str] = None
    assigned_user: Optional[dict] = None


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    actual_hours: Optional[float] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[str] = None
    assigned_to: Optional[str] = None


# ============================================================
# MEETING SCHEMAS
# ============================================================
class MeetingCreate(BaseModel):
    title: str
    project_id: Optional[str] = None
    team_id: Optional[str] = None
    transcript: str
    duration_minutes: Optional[int] = None


class MeetingResponse(BaseModel):
    id: str
    title: str
    project_id: Optional[str] = None
    team_id: Optional[str] = None
    conducted_by: str
    transcript: str
    summary: Optional[str] = None
    action_items: Optional[Any] = []
    extracted_tasks: Optional[Any] = []
    meeting_date: Optional[str] = None
    duration_minutes: Optional[int] = None
    created_at: Optional[str] = None


# ============================================================
# FEEDBACK SCHEMAS
# ============================================================
class FeedbackCreate(BaseModel):
    task_id: Optional[str] = None
    project_id: Optional[str] = None
    content: str


class FeedbackResponse(BaseModel):
    id: str
    user_id: str
    task_id: Optional[str] = None
    project_id: Optional[str] = None
    content: str
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_details: Optional[Any] = None
    ai_analysis: Optional[str] = None
    feedback_date: Optional[str] = None
    created_at: Optional[str] = None
    user: Optional[dict] = None


# ============================================================
# REPORT SCHEMAS
# ============================================================
class ReportCreate(BaseModel):
    title: str
    report_type: ReportType = ReportType.WEEKLY
    project_id: Optional[str] = None
    team_id: Optional[str] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None


class ReportResponse(BaseModel):
    id: str
    title: str
    report_type: str = "weekly"
    project_id: Optional[str] = None
    team_id: Optional[str] = None
    generated_by: str
    content: Optional[Any] = None
    summary: Optional[str] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    pdf_url: Optional[str] = None
    created_at: Optional[str] = None


# ============================================================
# NOTIFICATION SCHEMAS
# ============================================================
class NotificationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    notification_type: str = "general"
    is_read: bool = False
    is_email_sent: bool = False
    related_task_id: Optional[str] = None
    related_project_id: Optional[str] = None
    created_at: Optional[str] = None


# ============================================================
# DASHBOARD SCHEMAS
# ============================================================
class DashboardStats(BaseModel):
    total_tasks: int = 0
    completed_tasks: int = 0
    pending_tasks: int = 0
    delayed_tasks: int = 0
    in_progress_tasks: int = 0
    total_projects: int = 0
    active_projects: int = 0
    total_teams: int = 0
    total_employees: int = 0
    average_performance: float = 0
    average_productivity: float = 0
    completion_rate: float = 0
    delay_rate: float = 0
    unread_notifications: int = 0


class PerformanceData(BaseModel):
    user_id: str
    full_name: str
    performance_score: float = 0
    productivity_score: float = 0
    tasks_completed: int = 0
    tasks_total: int = 0
    completion_rate: float = 0
