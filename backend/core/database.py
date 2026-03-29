"""
OrchestrAI Database Module
Manages Supabase client and local SQLite fallback for demo mode.
"""
import json
import sqlite3
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Any

from core.config import get_settings

settings = get_settings()

# Try to import supabase
try:
    from supabase import create_client, Client

    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False

DB_PATH = Path(__file__).parent.parent / "database" / "orchestrai.db"


class DemoDatabase:
    """SQLite-based demo database that mirrors Supabase API patterns."""

    def __init__(self):
        self.db_path = str(DB_PATH)
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        """Initialize SQLite database with schema."""
        conn = self._get_conn()
        try:
            conn.executescript(
                """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL DEFAULT '',
                full_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'employee',
                avatar_url TEXT,
                department TEXT,
                designation TEXT,
                phone TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS teams (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                manager_id TEXT NOT NULL REFERENCES users(id),
                color TEXT DEFAULT '#667eea',
                icon TEXT DEFAULT 'users',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS team_members (
                id TEXT PRIMARY KEY,
                team_id TEXT NOT NULL REFERENCES teams(id),
                user_id TEXT NOT NULL REFERENCES users(id),
                joined_at TEXT DEFAULT (datetime('now')),
                UNIQUE(team_id, user_id)
            );

            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                team_id TEXT NOT NULL REFERENCES teams(id),
                manager_id TEXT NOT NULL REFERENCES users(id),
                status TEXT DEFAULT 'planning',
                start_date TEXT,
                end_date TEXT,
                progress REAL DEFAULT 0,
                risk_score REAL DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                project_id TEXT NOT NULL REFERENCES projects(id),
                assigned_to TEXT REFERENCES users(id),
                assigned_by TEXT REFERENCES users(id),
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                deadline TEXT,
                completed_at TEXT,
                estimated_hours REAL,
                actual_hours REAL,
                delay_probability REAL DEFAULT 0,
                meeting_id TEXT,
                tags TEXT DEFAULT '[]',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS meetings (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                project_id TEXT REFERENCES projects(id),
                team_id TEXT REFERENCES teams(id),
                conducted_by TEXT NOT NULL REFERENCES users(id),
                transcript TEXT NOT NULL,
                summary TEXT,
                action_items TEXT DEFAULT '[]',
                extracted_tasks TEXT DEFAULT '[]',
                attendees TEXT DEFAULT '[]',
                meeting_date TEXT DEFAULT (datetime('now')),
                duration_minutes INTEGER,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id),
                task_id TEXT REFERENCES tasks(id),
                project_id TEXT REFERENCES projects(id),
                content TEXT NOT NULL,
                sentiment TEXT,
                sentiment_score REAL,
                sentiment_details TEXT DEFAULT '{}',
                ai_analysis TEXT,
                feedback_date TEXT DEFAULT (date('now')),
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS performance (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id),
                project_id TEXT REFERENCES projects(id),
                period_start TEXT NOT NULL,
                period_end TEXT NOT NULL,
                tasks_completed INTEGER DEFAULT 0,
                tasks_delayed INTEGER DEFAULT 0,
                tasks_total INTEGER DEFAULT 0,
                completion_rate REAL DEFAULT 0,
                delay_rate REAL DEFAULT 0,
                performance_score REAL DEFAULT 0,
                productivity_score REAL DEFAULT 0,
                quality_score REAL DEFAULT 0,
                collaboration_score REAL DEFAULT 0,
                ai_insights TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                report_type TEXT DEFAULT 'weekly',
                project_id TEXT REFERENCES projects(id),
                team_id TEXT REFERENCES teams(id),
                generated_by TEXT NOT NULL REFERENCES users(id),
                content TEXT DEFAULT '{}',
                summary TEXT,
                period_start TEXT,
                period_end TEXT,
                pdf_url TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id),
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT DEFAULT 'general',
                is_read INTEGER DEFAULT 0,
                is_email_sent INTEGER DEFAULT 0,
                related_task_id TEXT REFERENCES tasks(id),
                related_project_id TEXT REFERENCES projects(id),
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
            )
            conn.commit()
        finally:
            conn.close()

    def seed_demo_data(self):
        """Seed database with TechNova Solutions demo data."""
        conn = self._get_conn()
        try:
            # Check if data already exists
            existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            if existing > 0:
                return

            from core.security import hash_password

            default_pw = hash_password("demo123")

            # Users
            users = [
                ("a0000000-0000-0000-0000-000000000001", "rahul.sharma@technova.com", default_pw, "Rahul Sharma", "manager", "Engineering", "Engineering Manager"),
                ("a0000000-0000-0000-0000-000000000002", "priya.patel@technova.com", default_pw, "Priya Patel", "employee", "AI Team", "ML Engineer"),
                ("a0000000-0000-0000-0000-000000000003", "amit.kumar@technova.com", default_pw, "Amit Kumar", "employee", "AI Team", "Data Scientist"),
                ("a0000000-0000-0000-0000-000000000004", "sneha.gupta@technova.com", default_pw, "Sneha Gupta", "employee", "AI Team", "AI Research Engineer"),
                ("a0000000-0000-0000-0000-000000000005", "vikram.singh@technova.com", default_pw, "Vikram Singh", "employee", "Web Team", "Senior Frontend Developer"),
                ("a0000000-0000-0000-0000-000000000006", "ananya.reddy@technova.com", default_pw, "Ananya Reddy", "employee", "Web Team", "UI/UX Designer"),
                ("a0000000-0000-0000-0000-000000000007", "rajesh.nair@technova.com", default_pw, "Rajesh Nair", "employee", "Web Team", "Frontend Developer"),
                ("a0000000-0000-0000-0000-000000000008", "deepika.joshi@technova.com", default_pw, "Deepika Joshi", "employee", "Backend Team", "Backend Developer"),
                ("a0000000-0000-0000-0000-000000000009", "arjun.menon@technova.com", default_pw, "Arjun Menon", "employee", "Backend Team", "DevOps Engineer"),
                ("a0000000-0000-0000-0000-000000000010", "kavya.iyer@technova.com", default_pw, "Kavya Iyer", "employee", "Backend Team", "Backend Developer"),
                ("a0000000-0000-0000-0000-000000000011", "nikhil.das@technova.com", default_pw, "Nikhil Das", "employee", "AI Team", "NLP Specialist"),
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO users (id, email, password_hash, full_name, role, department, designation) VALUES (?,?,?,?,?,?,?)",
                users,
            )

            # Teams
            teams = [
                ("b0000000-0000-0000-0000-000000000001", "AI Team", "Artificial Intelligence and Machine Learning division", "a0000000-0000-0000-0000-000000000001", "#667eea"),
                ("b0000000-0000-0000-0000-000000000002", "Web Team", "Frontend development team", "a0000000-0000-0000-0000-000000000001", "#00d4ff"),
                ("b0000000-0000-0000-0000-000000000003", "Backend Team", "Backend infrastructure team", "a0000000-0000-0000-0000-000000000001", "#764ba2"),
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO teams (id, name, description, manager_id, color) VALUES (?,?,?,?,?)",
                teams,
            )

            # Team Members
            members = [
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000002"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000003"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000004"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000011"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000005"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000006"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000007"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000008"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000009"),
                (str(uuid.uuid4()), "b0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000010"),
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO team_members (id, team_id, user_id) VALUES (?,?,?)",
                members,
            )

            # Projects
            projects = [
                ("c0000000-0000-0000-0000-000000000001", "SmartChat AI Assistant", "Build an intelligent customer support chatbot using NLP and transformer models.", "b0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000001", "active", "2026-01-15", "2026-04-30", 45),
                ("c0000000-0000-0000-0000-000000000002", "TechNova Web Portal Redesign", "Complete redesign of the company web portal with modern UI/UX.", "b0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000001", "active", "2026-02-01", "2026-05-15", 30),
                ("c0000000-0000-0000-0000-000000000003", "Microservices Migration", "Migrate monolithic backend to microservices architecture.", "b0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000001", "active", "2026-01-01", "2026-06-30", 55),
                ("c0000000-0000-0000-0000-000000000004", "Predictive Analytics Dashboard", "Develop real-time analytics dashboard with ML-powered predictions.", "b0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000001", "planning", "2026-04-01", "2026-07-31", 0),
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO projects (id, name, description, team_id, manager_id, status, start_date, end_date, progress) VALUES (?,?,?,?,?,?,?,?,?)",
                projects,
            )

            # Tasks
            tasks = [
                ("d0000000-0000-0000-0000-000000000001", "Train NLP model for intent classification", "Fine-tune BERT model for customer intent classification.", "c0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000001", "in_progress", "high", "2026-04-10", 40, 0.2),
                ("d0000000-0000-0000-0000-000000000002", "Build conversation flow engine", "Design and implement multi-turn conversation management.", "c0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000001", "in_progress", "high", "2026-04-15", 35, 0.15),
                ("d0000000-0000-0000-0000-000000000003", "Implement sentiment detection", "Create real-time sentiment analysis for messages.", "c0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000004", "a0000000-0000-0000-0000-000000000001", "pending", "medium", "2026-04-20", 25, 0.1),
                ("d0000000-0000-0000-0000-000000000004", "Knowledge base integration", "Connect chatbot with company knowledge base.", "c0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000011", "a0000000-0000-0000-0000-000000000001", "pending", "critical", "2026-04-25", 50, 0.35),
                ("d0000000-0000-0000-0000-000000000005", "Design new landing page", "Create modern glassmorphic landing page.", "c0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000006", "a0000000-0000-0000-0000-000000000001", "completed", "high", "2026-03-15", 20, 0),
                ("d0000000-0000-0000-0000-000000000006", "Implement responsive dashboard", "Build responsive dashboard with charts.", "c0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000005", "a0000000-0000-0000-0000-000000000001", "in_progress", "high", "2026-04-10", 30, 0.25),
                ("d0000000-0000-0000-0000-000000000007", "Build component library", "Create reusable React component library.", "c0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000007", "a0000000-0000-0000-0000-000000000001", "in_progress", "medium", "2026-04-05", 25, 0.1),
                ("d0000000-0000-0000-0000-000000000008", "Containerize services", "Create Dockerfiles for all microservices.", "c0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000009", "a0000000-0000-0000-0000-000000000001", "completed", "critical", "2026-03-01", 35, 0),
                ("d0000000-0000-0000-0000-000000000009", "Build API gateway", "Implement API gateway with rate limiting.", "c0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000008", "a0000000-0000-0000-0000-000000000001", "in_progress", "high", "2026-04-15", 45, 0.3),
                ("d0000000-0000-0000-0000-000000000010", "Set up CI/CD pipeline", "Configure GitHub Actions for automated deployment.", "c0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000009", "a0000000-0000-0000-0000-000000000001", "completed", "high", "2026-03-10", 20, 0),
                ("d0000000-0000-0000-0000-000000000011", "Database migration scripts", "Write migration scripts for PostgreSQL.", "c0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000010", "a0000000-0000-0000-0000-000000000001", "delayed", "high", "2026-03-20", 15, 0.8),
                ("d0000000-0000-0000-0000-000000000012", "Performance load testing", "Run load tests and optimize response times.", "c0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000010", "a0000000-0000-0000-0000-000000000001", "pending", "medium", "2026-04-30", 20, 0.4),
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO tasks (id, title, description, project_id, assigned_to, assigned_by, status, priority, deadline, estimated_hours, delay_probability) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                tasks,
            )

            # Meetings
            conn.execute(
                "INSERT OR IGNORE INTO meetings (id, title, project_id, team_id, conducted_by, transcript, summary, meeting_date, duration_minutes) VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    "e0000000-0000-0000-0000-000000000001",
                    "AI Team Sprint Planning",
                    "c0000000-0000-0000-0000-000000000001",
                    "b0000000-0000-0000-0000-000000000001",
                    "a0000000-0000-0000-0000-000000000001",
                    "Meeting started at 10:00 AM. Rahul: Welcome team. Let's discuss the SmartChat progress. Priya: The intent classification model is at 92% accuracy. Need another week to reach 95%. Amit: The conversation flow engine is 60% complete. Sneha: Haven't started sentiment detection yet. Nikhil: RAG architecture design is ready. Priorities: 1) Priya finish NLP training 2) Amit complete conversation engine 3) Sneha start sentiment module 4) Nikhil begin RAG implementation.",
                    "Sprint planning for SmartChat AI Assistant. NLP model at 92% accuracy, conversation engine 60% done. Key priorities set for all team members.",
                    "2026-03-25T10:00:00",
                    60,
                ),
            )

            # Feedback
            feedback_data = [
                ("f0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000002", "d0000000-0000-0000-0000-000000000001", "c0000000-0000-0000-0000-000000000001", "Good progress on the NLP model today. Accuracy improved to 92%. Feeling confident.", "positive", 0.85, "2026-03-27"),
                ("f0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000003", "d0000000-0000-0000-0000-000000000002", "c0000000-0000-0000-0000-000000000001", "Conversation flow engine is complex. Debugging context retention issues. Slower than expected.", "neutral", 0.5, "2026-03-27"),
                ("f0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000005", "d0000000-0000-0000-0000-000000000006", "c0000000-0000-0000-0000-000000000002", "Dashboard charts are looking great! Integrated three new chart types today.", "positive", 0.9, "2026-03-27"),
                ("f0000000-0000-0000-0000-000000000004", "a0000000-0000-0000-0000-000000000010", "d0000000-0000-0000-0000-000000000011", "c0000000-0000-0000-0000-000000000003", "Struggling with migration scripts. Legacy schema has undocumented dependencies. Frustrating.", "negative", 0.25, "2026-03-27"),
                ("f0000000-0000-0000-0000-000000000005", "a0000000-0000-0000-0000-000000000009", "d0000000-0000-0000-0000-000000000008", "c0000000-0000-0000-0000-000000000003", "Completed Docker containerization ahead of schedule. Great week!", "positive", 0.95, "2026-03-27"),
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO feedback (id, user_id, task_id, project_id, content, sentiment, sentiment_score, feedback_date) VALUES (?,?,?,?,?,?,?,?)",
                feedback_data,
            )

            # Performance
            perf_data = [
                ("g0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000002", "c0000000-0000-0000-0000-000000000001", "2026-03-01", "2026-03-31", 3, 0, 4, 75, 0, 85, 88),
                ("g0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000003", "c0000000-0000-0000-0000-000000000001", "2026-03-01", "2026-03-31", 2, 0, 3, 66, 0, 72, 70),
                ("g0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000005", "c0000000-0000-0000-0000-000000000002", "2026-03-01", "2026-03-31", 4, 1, 5, 80, 20, 78, 82),
                ("g0000000-0000-0000-0000-000000000004", "a0000000-0000-0000-0000-000000000009", "c0000000-0000-0000-0000-000000000003", "2026-03-01", "2026-03-31", 5, 0, 5, 100, 0, 96, 95),
                ("g0000000-0000-0000-0000-000000000005", "a0000000-0000-0000-0000-000000000010", "c0000000-0000-0000-0000-000000000003", "2026-03-01", "2026-03-31", 1, 1, 3, 33, 33, 45, 50),
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO performance (id, user_id, project_id, period_start, period_end, tasks_completed, tasks_delayed, tasks_total, completion_rate, delay_rate, performance_score, productivity_score) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                perf_data,
            )

            # Notifications
            notif_data = [
                ("i0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000002", "Task Deadline Approaching", "Your task 'Train NLP model' is due on April 10.", "deadline", 0),
                ("i0000000-0000-0000-0000-000000000002", "a0000000-0000-0000-0000-000000000010", "Task Delayed Alert", "Your task 'Database migration scripts' has been marked as delayed.", "delay", 0),
                ("i0000000-0000-0000-0000-000000000003", "a0000000-0000-0000-0000-000000000009", "Performance Recognition", "Congratulations! You achieved 100% task completion rate this month.", "performance", 1),
                ("i0000000-0000-0000-0000-000000000004", "a0000000-0000-0000-0000-000000000001", "Risk Alert", "Project 'Microservices Migration' has a potential delay risk.", "general", 0),
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO notifications (id, user_id, title, message, notification_type, is_read) VALUES (?,?,?,?,?,?)",
                notif_data,
            )

            # Reports
            conn.execute(
                "INSERT OR IGNORE INTO reports (id, title, report_type, project_id, team_id, generated_by, summary, period_start, period_end) VALUES (?,?,?,?,?,?,?,?,?)",
                ("h0000000-0000-0000-0000-000000000001", "AI Team Weekly Report - Week 12", "weekly", "c0000000-0000-0000-0000-000000000001", "b0000000-0000-0000-0000-000000000001", "a0000000-0000-0000-0000-000000000001", "AI Team made solid progress this week. NLP model accuracy improved to 92%.", "2026-03-17", "2026-03-23"),
            )

            conn.commit()
            print("Demo data seeded successfully - TechNova Solutions")
        except Exception as e:
            print(f"Seed data error: {e}")
            conn.rollback()
        finally:
            conn.close()

    def query(self, table: str):
        """Returns a QueryBuilder for the given table."""
        return QueryBuilder(self, table)


class QueryBuilder:
    """Fluent query builder that mimics Supabase Python client API."""

    def __init__(self, db: DemoDatabase, table: str):
        self.db = db
        self.table = table
        self._select_cols = "*"
        self._filters = []
        self._filter_vals = []
        self._order_col = None
        self._order_desc = False
        self._limit_val = None
        self._insert_data = None
        self._update_data = None
        self._delete = False

    def select(self, cols: str = "*"):
        self._select_cols = cols
        return self

    def eq(self, col: str, val: Any):
        self._filters.append(f"{col} = ?")
        self._filter_vals.append(val)
        return self

    def neq(self, col: str, val: Any):
        self._filters.append(f"{col} != ?")
        self._filter_vals.append(val)
        return self

    def gt(self, col: str, val: Any):
        self._filters.append(f"{col} > ?")
        self._filter_vals.append(val)
        return self

    def gte(self, col: str, val: Any):
        self._filters.append(f"{col} >= ?")
        self._filter_vals.append(val)
        return self

    def lt(self, col: str, val: Any):
        self._filters.append(f"{col} < ?")
        self._filter_vals.append(val)
        return self

    def lte(self, col: str, val: Any):
        self._filters.append(f"{col} <= ?")
        self._filter_vals.append(val)
        return self

    def like(self, col: str, pattern: str):
        self._filters.append(f"{col} LIKE ?")
        self._filter_vals.append(pattern)
        return self

    def ilike(self, col: str, pattern: str):
        self._filters.append(f"LOWER({col}) LIKE LOWER(?)")
        self._filter_vals.append(pattern)
        return self

    def in_(self, col: str, values: list):
        placeholders = ",".join("?" * len(values))
        self._filters.append(f"{col} IN ({placeholders})")
        self._filter_vals.extend(values)
        return self

    def order(self, col: str, desc: bool = False):
        self._order_col = col
        self._order_desc = desc
        return self

    def limit(self, count: int):
        self._limit_val = count
        return self

    def insert(self, data: dict | list):
        self._insert_data = data if isinstance(data, list) else [data]
        return self

    def update(self, data: dict):
        self._update_data = data
        return self

    def delete(self):
        self._delete = True
        return self

    def execute(self):
        conn = self.db._get_conn()
        try:
            if self._insert_data:
                return self._exec_insert(conn)
            elif self._update_data:
                return self._exec_update(conn)
            elif self._delete:
                return self._exec_delete(conn)
            else:
                return self._exec_select(conn)
        finally:
            conn.close()

    def _exec_select(self, conn):
        where = " AND ".join(self._filters) if self._filters else "1=1"
        sql = f"SELECT {self._select_cols} FROM {self.table} WHERE {where}"
        if self._order_col:
            sql += f" ORDER BY {self._order_col} {'DESC' if self._order_desc else 'ASC'}"
        if self._limit_val:
            sql += f" LIMIT {self._limit_val}"
        rows = conn.execute(sql, self._filter_vals).fetchall()
        data = [dict(r) for r in rows]
        return type("Response", (), {"data": data, "count": len(data)})()

    def _exec_insert(self, conn):
        results = []
        for item in self._insert_data:
            if "id" not in item:
                item["id"] = str(uuid.uuid4())
            cols = ", ".join(item.keys())
            placeholders = ", ".join("?" * len(item))
            sql = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"
            conn.execute(sql, list(item.values()))
            results.append(item)
        conn.commit()
        return type("Response", (), {"data": results, "count": len(results)})()

    def _exec_update(self, conn):
        set_clause = ", ".join(f"{k} = ?" for k in self._update_data.keys())
        where = " AND ".join(self._filters) if self._filters else "1=1"
        vals = list(self._update_data.values()) + self._filter_vals
        sql = f"UPDATE {self.table} SET {set_clause} WHERE {where}"
        conn.execute(sql, vals)
        conn.commit()
        # Return updated rows
        select_where = " AND ".join(self._filters) if self._filters else "1=1"
        rows = conn.execute(
            f"SELECT * FROM {self.table} WHERE {select_where}", self._filter_vals
        ).fetchall()
        data = [dict(r) for r in rows]
        return type("Response", (), {"data": data, "count": len(data)})()

    def _exec_delete(self, conn):
        where = " AND ".join(self._filters) if self._filters else "1=1"
        # Get rows before delete
        rows = conn.execute(
            f"SELECT * FROM {self.table} WHERE {where}", self._filter_vals
        ).fetchall()
        data = [dict(r) for r in rows]
        conn.execute(
            f"DELETE FROM {self.table} WHERE {where}", self._filter_vals
        )
        conn.commit()
        return type("Response", (), {"data": data, "count": len(data)})()


# Global database instance
_db_instance: Optional[DemoDatabase] = None
_supabase_client = None


def get_database():
    """Get database instance (Supabase or Demo SQLite)."""
    global _db_instance, _supabase_client

    if settings.DEMO_MODE or not settings.SUPABASE_URL:
        if _db_instance is None:
            _db_instance = DemoDatabase()
            _db_instance.seed_demo_data()
        return _db_instance
    else:
        if _supabase_client is None and HAS_SUPABASE:
            _supabase_client = create_client(
                settings.SUPABASE_URL, settings.SUPABASE_KEY
            )
        return _supabase_client


def get_db():
    """FastAPI dependency for database access."""
    return get_database()
