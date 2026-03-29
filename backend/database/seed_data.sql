-- ============================================================
-- OrchestrAI Seed Data - TechNova Solutions
-- ============================================================

-- USERS (Manager + 10 Employees)
INSERT INTO users (id, email, full_name, role, department, designation) VALUES
('a0000000-0000-0000-0000-000000000001', 'rahul.sharma@technova.com', 'Rahul Sharma', 'manager', 'Engineering', 'Engineering Manager'),
('a0000000-0000-0000-0000-000000000002', 'priya.patel@technova.com', 'Priya Patel', 'employee', 'AI Team', 'ML Engineer'),
('a0000000-0000-0000-0000-000000000003', 'amit.kumar@technova.com', 'Amit Kumar', 'employee', 'AI Team', 'Data Scientist'),
('a0000000-0000-0000-0000-000000000004', 'sneha.gupta@technova.com', 'Sneha Gupta', 'employee', 'AI Team', 'AI Research Engineer'),
('a0000000-0000-0000-0000-000000000005', 'vikram.singh@technova.com', 'Vikram Singh', 'employee', 'Web Team', 'Senior Frontend Developer'),
('a0000000-0000-0000-0000-000000000006', 'ananya.reddy@technova.com', 'Ananya Reddy', 'employee', 'Web Team', 'UI/UX Designer'),
('a0000000-0000-0000-0000-000000000007', 'rajesh.nair@technova.com', 'Rajesh Nair', 'employee', 'Web Team', 'Frontend Developer'),
('a0000000-0000-0000-0000-000000000008', 'deepika.joshi@technova.com', 'Deepika Joshi', 'employee', 'Backend Team', 'Backend Developer'),
('a0000000-0000-0000-0000-000000000009', 'arjun.menon@technova.com', 'Arjun Menon', 'employee', 'Backend Team', 'DevOps Engineer'),
('a0000000-0000-0000-0000-000000000010', 'kavya.iyer@technova.com', 'Kavya Iyer', 'employee', 'Backend Team', 'Backend Developer'),
('a0000000-0000-0000-0000-000000000011', 'nikhil.das@technova.com', 'Nikhil Das', 'employee', 'AI Team', 'NLP Specialist');

-- TEAMS
INSERT INTO teams (id, name, description, manager_id, color) VALUES
('b0000000-0000-0000-0000-000000000001', 'AI Team', 'Artificial Intelligence and Machine Learning division focused on NLP, computer vision, and predictive analytics.', 'a0000000-0000-0000-0000-000000000001', '#667eea'),
('b0000000-0000-0000-0000-000000000002', 'Web Team', 'Frontend development team responsible for client-facing web applications and UI/UX.', 'a0000000-0000-0000-0000-000000000001', '#00d4ff'),
('b0000000-0000-0000-0000-000000000003', 'Backend Team', 'Backend infrastructure team managing APIs, databases, and cloud services.', 'a0000000-0000-0000-0000-000000000001', '#764ba2');

-- TEAM MEMBERS
INSERT INTO team_members (team_id, user_id) VALUES
('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002'),
('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000003'),
('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000004'),
('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000011'),
('b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000005'),
('b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000006'),
('b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000007'),
('b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000008'),
('b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000009'),
('b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000010');

-- PROJECTS
INSERT INTO projects (id, name, description, team_id, manager_id, status, start_date, end_date, progress) VALUES
('c0000000-0000-0000-0000-000000000001', 'SmartChat AI Assistant', 'Build an intelligent customer support chatbot using NLP and transformer models.', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'active', '2026-01-15', '2026-04-30', 45),
('c0000000-0000-0000-0000-000000000002', 'TechNova Web Portal Redesign', 'Complete redesign of the company web portal with modern UI/UX.', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'active', '2026-02-01', '2026-05-15', 30),
('c0000000-0000-0000-0000-000000000003', 'Microservices Migration', 'Migrate monolithic backend to microservices architecture on Kubernetes.', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'active', '2026-01-01', '2026-06-30', 55),
('c0000000-0000-0000-0000-000000000004', 'Predictive Analytics Dashboard', 'Develop real-time analytics dashboard with ML-powered predictions.', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'planning', '2026-04-01', '2026-07-31', 0);

-- TASKS
INSERT INTO tasks (id, title, description, project_id, assigned_to, assigned_by, status, priority, deadline, estimated_hours, delay_probability) VALUES
('d0000000-0000-0000-0000-000000000001', 'Train NLP model for intent classification', 'Fine-tune BERT model for customer intent classification with 95%+ accuracy.', 'c0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'in_progress', 'high', '2026-04-10', 40, 0.2),
('d0000000-0000-0000-0000-000000000002', 'Build conversation flow engine', 'Design and implement multi-turn conversation management system.', 'c0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'in_progress', 'high', '2026-04-15', 35, 0.15),
('d0000000-0000-0000-0000-000000000003', 'Implement sentiment detection module', 'Create real-time sentiment analysis for customer messages.', 'c0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000001', 'pending', 'medium', '2026-04-20', 25, 0.1),
('d0000000-0000-0000-0000-000000000004', 'Knowledge base integration', 'Connect chatbot with company knowledge base using RAG architecture.', 'c0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001', 'pending', 'critical', '2026-04-25', 50, 0.35),
('d0000000-0000-0000-0000-000000000005', 'Design new landing page', 'Create modern glassmorphic landing page design with animations.', 'c0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000006', 'a0000000-0000-0000-0000-000000000001', 'completed', 'high', '2026-03-15', 20, 0),
('d0000000-0000-0000-0000-000000000006', 'Implement responsive dashboard', 'Build responsive dashboard with Chart.js and real-time data.', 'c0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000005', 'a0000000-0000-0000-0000-000000000001', 'in_progress', 'high', '2026-04-10', 30, 0.25),
('d0000000-0000-0000-0000-000000000007', 'Build component library', 'Create reusable React component library with Storybook docs.', 'c0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000007', 'a0000000-0000-0000-0000-000000000001', 'in_progress', 'medium', '2026-04-05', 25, 0.1),
('d0000000-0000-0000-0000-000000000008', 'Containerize services with Docker', 'Create Dockerfiles and docker-compose for all microservices.', 'c0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000009', 'a0000000-0000-0000-0000-000000000001', 'completed', 'critical', '2026-03-01', 35, 0),
('d0000000-0000-0000-0000-000000000009', 'Build API gateway', 'Implement API gateway with rate limiting, auth, and load balancing.', 'c0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000008', 'a0000000-0000-0000-0000-000000000001', 'in_progress', 'high', '2026-04-15', 45, 0.3),
('d0000000-0000-0000-0000-000000000010', 'Set up CI/CD pipeline', 'Configure GitHub Actions with automated testing and deployment.', 'c0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000009', 'a0000000-0000-0000-0000-000000000001', 'completed', 'high', '2026-03-10', 20, 0),
('d0000000-0000-0000-0000-000000000011', 'Database migration scripts', 'Write migration scripts for PostgreSQL to support new schema.', 'c0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'delayed', 'high', '2026-03-20', 15, 0.8),
('d0000000-0000-0000-0000-000000000012', 'Performance load testing', 'Run load tests and optimize API response times below 200ms.', 'c0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000001', 'pending', 'medium', '2026-04-30', 20, 0.4);

-- MEETINGS
INSERT INTO meetings (id, title, project_id, team_id, conducted_by, transcript, summary, meeting_date, duration_minutes) VALUES
('e0000000-0000-0000-0000-000000000001', 'AI Team Sprint Planning', 'c0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001',
'Meeting started at 10:00 AM. Rahul: Welcome team. Let''s discuss the SmartChat progress. Priya, how is the NLP model training? Priya: The intent classification model is at 92% accuracy. Need another week to reach 95%. Amit: The conversation flow engine is 60% complete. I''m working on context retention. Sneha: I haven''t started on sentiment detection yet. Will begin next week. Nikhil: The knowledge base RAG architecture design is ready but implementation needs more resources. Rahul: OK, priorities are: 1) Priya finish NLP training 2) Amit complete conversation engine 3) Sneha start sentiment module 4) Nikhil begin RAG implementation. Any blockers? Priya: Need access to more training data. Amit: Need API docs for the customer system. Meeting ended at 11:00 AM.',
'Sprint planning for SmartChat AI Assistant. NLP model at 92% accuracy, conversation engine 60% done. Key priorities: complete NLP training, finish conversation engine, start sentiment module, begin RAG implementation. Blockers identified: training data access and API documentation needed.',
'2026-03-25 10:00:00+05:30', 60),

('e0000000-0000-0000-0000-000000000002', 'Web Team Design Review', 'c0000000-0000-0000-0000-000000000002', 'b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001',
'Meeting started at 2:00 PM. Rahul: Let''s review the web portal redesign. Ananya, show us the new designs. Ananya: I''ve completed the landing page and dashboard mockups. Using glassmorphism with dark theme. Vikram: The dashboard implementation is going well. Charts are responsive. Need to add real-time updates. Rajesh: Component library is 70% done. Working on form components now. Rahul: Great progress. Action items: 1) Vikram add real-time WebSocket updates 2) Rajesh complete form components 3) Ananya design the analytics page. Timeline is tight, let''s stay focused. Meeting ended at 3:00 PM.',
'Design review for web portal redesign. Landing page and dashboard mockups completed with glassmorphism dark theme. Dashboard implementation progressing with responsive charts. Component library 70% complete. Action items: add WebSocket updates, complete form components, design analytics page.',
'2026-03-26 14:00:00+05:30', 60);

-- FEEDBACK
INSERT INTO feedback (id, user_id, task_id, project_id, content, sentiment, sentiment_score, feedback_date) VALUES
('f0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002', 'd0000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', 'Good progress on the NLP model today. Accuracy improved from 90% to 92%. Feeling confident about hitting the target. Need more diverse training data to push past 94%.', 'positive', 0.85, '2026-03-27'),
('f0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000003', 'd0000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001', 'Conversation flow engine is complex. Spent most of the day debugging context retention issues. Making progress but slower than expected. Might need to revise the architecture.', 'neutral', 0.5, '2026-03-27'),
('f0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000005', 'd0000000-0000-0000-0000-000000000006', 'c0000000-0000-0000-0000-000000000002', 'Dashboard charts are looking great! Integrated three new chart types today. Real-time updates will be the next challenge but I have a solid plan.', 'positive', 0.9, '2026-03-27'),
('f0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000010', 'd0000000-0000-0000-0000-000000000011', 'c0000000-0000-0000-0000-000000000003', 'Struggling with the migration scripts. Legacy schema has undocumented dependencies. This is frustrating and will likely cause delays. Need help from someone who knows the old system.', 'negative', 0.25, '2026-03-27'),
('f0000000-0000-0000-0000-000000000005', 'a0000000-0000-0000-0000-000000000009', 'd0000000-0000-0000-0000-000000000008', 'c0000000-0000-0000-0000-000000000003', 'Completed Docker containerization ahead of schedule. All services are running smoothly in containers. CI/CD pipeline also fully operational. Great week overall!', 'positive', 0.95, '2026-03-27'),
('f0000000-0000-0000-0000-000000000006', 'a0000000-0000-0000-0000-000000000008', 'd0000000-0000-0000-0000-000000000009', 'c0000000-0000-0000-0000-000000000003', 'API gateway is taking longer than expected. Rate limiting logic is tricky with our distributed setup. Feeling a bit overwhelmed with the scope of work.', 'negative', 0.3, '2026-03-27');

-- PERFORMANCE
INSERT INTO performance (id, user_id, project_id, period_start, period_end, tasks_completed, tasks_delayed, tasks_total, completion_rate, delay_rate, performance_score, productivity_score) VALUES
('g0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001', '2026-03-01', '2026-03-31', 3, 0, 4, 75, 0, 85, 88),
('g0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000001', '2026-03-01', '2026-03-31', 2, 0, 3, 66, 0, 72, 70),
('g0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000002', '2026-03-01', '2026-03-31', 4, 1, 5, 80, 20, 78, 82),
('g0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000009', 'c0000000-0000-0000-0000-000000000003', '2026-03-01', '2026-03-31', 5, 0, 5, 100, 0, 96, 95),
('g0000000-0000-0000-0000-000000000005', 'a0000000-0000-0000-0000-000000000010', 'c0000000-0000-0000-0000-000000000003', '2026-03-01', '2026-03-31', 1, 1, 3, 33, 33, 45, 50);

-- REPORTS
INSERT INTO reports (id, title, report_type, project_id, team_id, generated_by, summary, period_start, period_end) VALUES
('h0000000-0000-0000-0000-000000000001', 'AI Team Weekly Report - Week 12', 'weekly', 'c0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'AI Team made solid progress this week. NLP model accuracy improved to 92%. Conversation engine at 60% completion. Key risk: knowledge base implementation needs more resources. Team morale is generally positive with one concern about project scope.', '2026-03-17', '2026-03-23'),
('h0000000-0000-0000-0000-000000000002', 'Backend Team Monthly Report - March', 'monthly', 'c0000000-0000-0000-0000-000000000003', 'b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'Backend Team completed Docker containerization and CI/CD pipeline setup. API gateway development in progress. Database migration scripts facing delays due to legacy schema complexity. Overall project at 55% completion. One team member showing signs of stress - recommend workload review.', '2026-03-01', '2026-03-31');

-- NOTIFICATIONS  
INSERT INTO notifications (id, user_id, title, message, notification_type, is_read) VALUES
('i0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000002', 'Task Deadline Approaching', 'Your task "Train NLP model for intent classification" is due on April 10.', 'deadline', false),
('i0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000010', 'Task Delayed Alert', 'Your task "Database migration scripts" has been marked as delayed.', 'delay', false),
('i0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000009', 'Performance Recognition', 'Congratulations! You achieved 100% task completion rate this month.', 'performance', true),
('i0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000001', 'Risk Alert', 'Project "Microservices Migration" has a potential delay risk due to migration script issues.', 'general', false);
