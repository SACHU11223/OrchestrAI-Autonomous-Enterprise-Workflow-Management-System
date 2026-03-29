import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'

export default function TaskManagement() {
  const { user } = useAuth()
  const [tasks, setTasks] = useState([])
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => { fetchTasks() }, [user])

  useEffect(() => {
    const handleTaskUpdate = (e) => {
      console.log('Realtime task update received:', e.detail)
      fetchTasks() // Refetch silently
    }
    window.addEventListener('orchestrai:task_updated', handleTaskUpdate)
    return () => window.removeEventListener('orchestrai:task_updated', handleTaskUpdate)
  }, [user])

  const fetchTasks = async () => {
    try {
      const endpoint = user?.role === 'manager' ? '/api/tasks' : '/api/tasks/my'
      const [t, p] = await Promise.all([api.get(endpoint), api.get('/api/projects')])
      setTasks(t.data)
      setProjects(p.data)
    } catch {} finally { setLoading(false) }
  }

  const updateStatus = async (taskId, newStatus) => {
    try {
      await api.patch(`/api/tasks/${taskId}`, { status: newStatus })
      fetchTasks()
    } catch (err) { alert('Error updating task') }
  }

  const filteredTasks = filter === 'all' ? tasks : tasks.filter(t => t.status === filter)

  const statusConfig = {
    pending: { color: 'warning', label: 'Pending', icon: '⏳' },
    in_progress: { color: 'info', label: 'In Progress', icon: '⚡' },
    completed: { color: 'success', label: 'Completed', icon: '✅' },
    delayed: { color: 'danger', label: 'Delayed', icon: '⚠️' },
  }

  const priorityConfig = {
    low: { color: 'neutral', icon: '🟢' },
    medium: { color: 'primary', icon: '🔵' },
    high: { color: 'warning', icon: '🟠' },
    critical: { color: 'danger', icon: '🔴' },
  }

  if (loading) return <div className="loader"><div className="loader-spinner" /></div>

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title"><span className="page-title-icon">✅</span> Task Management</h1>
          <p className="page-subtitle">{user?.role === 'manager' ? 'All team tasks' : 'Your assigned tasks'}</p>
        </div>
      </div>

      {/* Filter Bar */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', flexWrap: 'wrap' }}>
        {['all', 'pending', 'in_progress', 'completed', 'delayed'].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`btn ${filter === f ? 'btn-primary' : 'btn-secondary'} btn-sm`}>
            {f === 'all' ? '📋 All' : `${statusConfig[f]?.icon} ${statusConfig[f]?.label}`}
            <span style={{ marginLeft: '6px', opacity: 0.7 }}>
              ({f === 'all' ? tasks.length : tasks.filter(t => t.status === f).length})
            </span>
          </button>
        ))}
      </div>

      {/* Task List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {filteredTasks.map(task => {
          const sc = statusConfig[task.status] || statusConfig.pending
          const pc = priorityConfig[task.priority] || priorityConfig.medium
          const project = projects.find(p => p.id === task.project_id)

          return (
            <div key={task.id} className="task-card">
              <div className="task-card-header">
                <div style={{ flex: 1 }}>
                  <div className="task-card-title">{task.title}</div>
                  {task.description && (
                    <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px', lineHeight: 1.5 }}>
                      {task.description.slice(0, 150)}
                    </p>
                  )}
                </div>
                <div style={{ display: 'flex', gap: '6px', flexShrink: 0 }}>
                  <span className={`badge badge-${pc.color}`}>{pc.icon} {task.priority}</span>
                  <span className={`badge badge-${sc.color}`}>{sc.icon} {sc.label}</span>
                </div>
              </div>

              <div className="task-card-meta">
                <span className="task-card-meta-item">📁 {project?.name || task.project_name || 'Unknown'}</span>
                {task.assigned_user && <span className="task-card-meta-item">👤 {task.assigned_user.full_name}</span>}
                {task.deadline && <span className="task-card-meta-item">📅 {task.deadline.split('T')[0]}</span>}
                {task.estimated_hours > 0 && <span className="task-card-meta-item">⏱️ {task.estimated_hours}h est.</span>}
                {task.delay_probability > 0.3 && (
                  <span className="task-card-meta-item" style={{ color: 'var(--accent-red)' }}>
                    🚨 {(task.delay_probability * 100).toFixed(0)}% delay risk
                  </span>
                )}
              </div>

              <div className="task-card-actions">
                {task.status !== 'completed' && (
                  <>
                    {task.status === 'pending' && (
                      <button className="btn btn-primary btn-sm" onClick={() => updateStatus(task.id, 'in_progress')}>
                        ▶️ Start
                      </button>
                    )}
                    {task.status === 'in_progress' && (
                      <button className="btn btn-success btn-sm" onClick={() => updateStatus(task.id, 'completed')}>
                        ✅ Complete
                      </button>
                    )}
                    {task.status === 'delayed' && (
                      <button className="btn btn-primary btn-sm" onClick={() => updateStatus(task.id, 'in_progress')}>
                        🔄 Resume
                      </button>
                    )}
                    {task.status !== 'delayed' && (
                      <button className="btn btn-danger btn-sm" onClick={() => updateStatus(task.id, 'delayed')}>
                        ⚠️ Mark Delayed
                      </button>
                    )}
                  </>
                )}
              </div>
            </div>
          )
        })}

        {filteredTasks.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">📋</div>
            <div className="empty-state-title">No tasks found</div>
            <div className="empty-state-description">
              {filter !== 'all' ? 'Try changing the filter' : 'Tasks will appear here after processing meetings'}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
