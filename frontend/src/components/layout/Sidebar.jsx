import { NavLink, useLocation } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

const managerNav = [
  { label: 'Overview', path: '/dashboard', icon: '📊' },
  { label: 'Teams', path: '/teams', icon: '👥' },
  { label: 'Projects', path: '/projects', icon: '📁' },
  { label: 'Meetings', path: '/meetings', icon: '🎙️' },
  { label: 'Video Call', path: '/video-conference', icon: '📹' },
  { label: 'Tasks', path: '/tasks', icon: '✅' },
  { label: 'Feedback', path: '/feedback', icon: '💬' },
  { label: 'Reports', path: '/reports', icon: '📄' },
  { label: 'Analytics', path: '/analytics', icon: '📈' },
]

const employeeNav = [
  { label: 'My Dashboard', path: '/my-dashboard', icon: '🏠' },
  { label: 'My Tasks', path: '/tasks', icon: '✅' },
  { label: 'Video Call', path: '/video-conference', icon: '📹' },
  { label: 'Feedback', path: '/feedback', icon: '💬' },
  { label: 'Reports', path: '/reports', icon: '📄' },
]

export default function Sidebar() {
  const { user, logout } = useAuth()
  const isManager = user?.role === 'manager'
  const nav = isManager ? managerNav : employeeNav

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">O</div>
        <div>
          <div className="sidebar-logo-text">OrchestrAI</div>
          <div style={{ fontSize: '10px', color: 'var(--text-tertiary)', letterSpacing: '1px' }}>
            WORKFLOW AI
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="sidebar-section-label">
          {isManager ? 'Management' : 'Workspace'}
        </div>
        {nav.map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}
          >
            <span className="sidebar-item-icon">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-user">
        <div className="sidebar-user-avatar">
          {user?.full_name?.charAt(0) || 'U'}
        </div>
        <div className="sidebar-user-info">
          <div className="sidebar-user-name">{user?.full_name || 'User'}</div>
          <div className="sidebar-user-role">{user?.role || 'employee'}</div>
        </div>
        <button
          className="btn btn-ghost btn-sm"
          onClick={logout}
          title="Logout"
          style={{ marginLeft: 'auto', fontSize: '16px' }}
        >
          🚪
        </button>
      </div>
    </aside>
  )
}
