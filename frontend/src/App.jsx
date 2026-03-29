import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { RealtimeProvider } from './contexts/RealtimeContext'
import Layout from './components/layout/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import ManagerDashboard from './pages/ManagerDashboard'
import EmployeeDashboard from './pages/EmployeeDashboard'
import TeamManagement from './pages/TeamManagement'
import ProjectPage from './pages/ProjectPage'
import MeetingInput from './pages/MeetingInput'
import TaskManagement from './pages/TaskManagement'
import FeedbackPage from './pages/FeedbackPage'
import ReportsPage from './pages/ReportsPage'
import AnalyticsDashboard from './pages/AnalyticsDashboard'
import VideoConference from './pages/VideoConference'

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="loader"><div className="loader-spinner" /></div>
  return user ? children : <Navigate to="/login" />
}

function AppRoutes() {
  const { user } = useAuth()
  const isManager = user?.role === 'manager'

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
        <Route index element={<Navigate to={isManager ? "/dashboard" : "/my-dashboard"} />} />
        <Route path="dashboard" element={<ManagerDashboard />} />
        <Route path="my-dashboard" element={<EmployeeDashboard />} />
        <Route path="teams" element={<TeamManagement />} />
        <Route path="projects" element={<ProjectPage />} />
        <Route path="meetings" element={<MeetingInput />} />
        <Route path="video-conference" element={<VideoConference />} />
        <Route path="tasks" element={<TaskManagement />} />
        <Route path="feedback" element={<FeedbackPage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="analytics" element={<AnalyticsDashboard />} />
      </Route>
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <RealtimeProvider>
          <AppRoutes />
        </RealtimeProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}
