"""
OrchestrAI - FastAPI Main Application
Autonomous Enterprise Workflow Management System
"""
import sys
import os
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from core.config import get_settings
from core.database import get_db

# Import routers
from api.auth import router as auth_router
from api.teams import router as teams_router
from api.projects import router as projects_router
from api.meetings import router as meetings_router
from api.tasks import router as tasks_router
from api.feedback import router as feedback_router
from api.reports import router as reports_router
from api.dashboard import router as dashboard_router
from api.notifications import router as notifications_router

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="OrchestrAI",
    description="Autonomous Enterprise Workflow Management System powered by Multi-Agent AI",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(teams_router)
app.include_router(projects_router)
app.include_router(meetings_router)
app.include_router(tasks_router)
app.include_router(feedback_router)
app.include_router(reports_router)
app.include_router(dashboard_router)
app.include_router(notifications_router)

from fastapi import WebSocket, WebSocketDisconnect
from core.websockets import manager

@app.websocket("/api/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Respond to ping to keep alive
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


@app.on_event("startup")
async def startup():
    """Initialize database and seed demo data on startup."""
    print("Starting OrchestrAI...")
    print(f"   Mode: {'DEMO' if settings.DEMO_MODE else 'PRODUCTION'}")
    print(f"   Gemini API: {'Configured' if settings.GEMINI_API_KEY else 'Not configured (using demo responses)'}")
    print(f"   Supabase: {'Configured' if settings.SUPABASE_URL else 'Not configured (using SQLite)'}")
    
    # Initialize database with demo data
    db = get_db()
    print("Database initialized")
    print("OrchestrAI is ready!")
    print("API Docs: http://localhost:8000/docs")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "OrchestrAI",
        "version": settings.APP_VERSION,
        "description": "Autonomous Enterprise Workflow Management System",
        "status": "running",
        "mode": "demo" if settings.DEMO_MODE else "production",
        "docs": "/docs",
        "company": "TechNova Solutions",
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/api/reports/{report_id}/pdf")
async def download_report_pdf(report_id: str):
    """Download a report as PDF."""
    import json
    from services.pdf_service import generate_report_pdf
    
    db = get_db()
    result = db.table("reports").select("*").eq("id", report_id).execute()
    if not result.data:
        return JSONResponse(status_code=404, content={"detail": "Report not found"})
    
    report = result.data[0]
    if isinstance(report.get("content"), str):
        try:
            report["content"] = json.loads(report["content"])
        except:
            pass
    
    pdf_bytes = generate_report_pdf(report)
    
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="orchestrai_report_{report_id[:8]}.pdf"'}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
