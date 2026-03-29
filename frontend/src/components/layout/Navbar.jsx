import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import api from '../../services/api'

const pageTitles = {
  '/dashboard': 'Manager Dashboard',
  '/my-dashboard': 'My Dashboard',
  '/teams': 'Team Management',
  '/projects': 'Projects',
  '/meetings': 'Meeting Hub',
  '/tasks': 'Task Management',
  '/feedback': 'Daily Feedback',
  '/reports': 'Reports',
  '/analytics': 'Analytics Dashboard',
}

import EditProfileModal from '../modals/EditProfileModal'

export default function Navbar() {
  const { user } = useAuth()
  const location = useLocation()
  const [notifications, setNotifications] = useState([])
  const [showNotifs, setShowNotifs] = useState(false)
  const [showProfileModal, setShowProfileModal] = useState(false)

  const title = pageTitles[location.pathname] || 'OrchestrAI'
  const unread = notifications.filter(n => !n.is_read).length

  useEffect(() => {
    fetchNotifications()
  }, [location.pathname])

  const fetchNotifications = async () => {
    try {
      const res = await api.get('/api/notifications')
      setNotifications(res.data.slice(0, 10))
    } catch {}
  }

  const markAllRead = async () => {
    try {
      await api.post('/api/notifications/mark-all-read')
      setNotifications(prev => prev.map(n => ({ ...n, is_read: 1 })))
    } catch {}
  }

  return (
    <header className="navbar">
      <div>
        <h1 className="navbar-title">{title}</h1>
      </div>
      <div className="navbar-actions">
        <div style={{ position: 'relative' }}>
          <button
            className="navbar-notification-btn"
            onClick={() => setShowNotifs(!showNotifs)}
            id="notification-toggle"
          >
            🔔
            {unread > 0 && (
              <span className="navbar-notification-badge">{unread}</span>
            )}
          </button>

          {showNotifs && (
            <div style={{
              position: 'absolute', top: '100%', right: 0, marginTop: '8px',
              width: '360px', background: 'var(--bg-secondary)', border: '1px solid var(--glass-border)',
              borderRadius: 'var(--radius-lg)', overflow: 'hidden', zIndex: 200,
              boxShadow: '0 20px 60px rgba(0,0,0,0.5)', animation: 'scaleIn 0.2s ease-out',
            }}>
              <div style={{
                padding: '16px 20px', borderBottom: '1px solid var(--glass-border)',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              }}>
                <span style={{ fontWeight: 700, fontSize: '14px' }}>Notifications</span>
                {unread > 0 && (
                  <button className="btn btn-ghost btn-sm" onClick={markAllRead}>
                    Mark all read
                  </button>
                )}
              </div>
              <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
                {notifications.length === 0 ? (
                  <div style={{ padding: '40px 20px', textAlign: 'center', color: 'var(--text-tertiary)', fontSize: '13px' }}>
                    No notifications yet
                  </div>
                ) : (
                  notifications.map(n => (
                    <div key={n.id} style={{
                      padding: '12px 20px', borderBottom: '1px solid rgba(255,255,255,0.03)',
                      background: n.is_read ? 'transparent' : 'rgba(102, 126, 234, 0.05)',
                      transition: 'background 0.15s',
                    }}>
                      <div style={{ fontWeight: 600, fontSize: '13px', marginBottom: '4px' }}>{n.title}</div>
                      <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', lineHeight: 1.5 }}>{n.message}</div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        <div 
          onClick={() => setShowProfileModal(true)}
          style={{
            display: 'flex', alignItems: 'center', gap: '10px',
            padding: '6px 14px', background: 'var(--glass-bg)', borderRadius: 'var(--radius-md)',
            border: '1px solid var(--glass-border)', cursor: 'pointer', transition: 'all 0.2s ease'
          }}
          className="hover-card"
        >
          <div style={{
            width: '30px', height: '30px', borderRadius: '50%',
            background: 'var(--accent-gradient)', display: 'flex',
            alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '13px',
          }}>
            {user?.full_name?.charAt(0) || 'U'}
          </div>
          <span style={{ fontSize: '13px', fontWeight: 600 }}>{user?.full_name}</span>
        </div>
      </div>
      
      {showProfileModal && (
        <EditProfileModal onClose={() => setShowProfileModal(false)} />
      )}
    </header>
  )
}
