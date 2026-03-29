import { useState, useEffect } from 'react'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Filler } from 'chart.js'
import { Doughnut, Line } from 'react-chartjs-2'
import api from '../services/api'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Filler)

export default function EmployeeDashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
    
    const handleSync = () => fetchData()
    window.addEventListener('orchestrai:sync', handleSync)
    return () => window.removeEventListener('orchestrai:sync', handleSync)
  }, [])

  const fetchData = async () => {
    try {
      const res = await api.get('/api/dashboard/employee')
      setData(res.data)
    } catch (err) { console.error(err) }
    finally { setLoading(false) }
  }

  if (loading) return <div className="loader"><div className="loader-spinner" /></div>
  if (!data) return <div className="empty-state"><div className="empty-state-icon">🏠</div><div className="empty-state-title">No data available</div></div>

  const { stats, tasks, performance, sentiment_trend } = data

  const taskData = {
    labels: ['Completed', 'In Progress', 'Pending', 'Delayed'],
    datasets: [{ data: [stats.completed_tasks, stats.in_progress_tasks, stats.pending_tasks, stats.delayed_tasks],
      backgroundColor: ['#00e676', '#667eea', '#ff9100', '#ff5252'], borderWidth: 0 }],
  }

  const sentimentData = {
    labels: sentiment_trend?.map((_, i) => `Day ${i+1}`) || [],
    datasets: [{ label: 'Sentiment', data: sentiment_trend || [], borderColor: '#667eea', backgroundColor: 'rgba(102,126,234,0.1)',
      fill: true, tension: 0.4, pointRadius: 4, pointBackgroundColor: '#667eea' }],
  }

  const statusColor = { pending: 'warning', in_progress: 'info', completed: 'success', delayed: 'danger' }
  const priorityColor = { low: 'neutral', medium: 'primary', high: 'warning', critical: 'danger' }

  return (
    <div>
      {/* Stats */}
      <div className="grid-stats">
        {[
          { label: 'My Tasks', value: stats.total_tasks, icon: '📋', color: 'blue' },
          { label: 'Completed', value: stats.completed_tasks, icon: '✅', color: 'green' },
          { label: 'In Progress', value: stats.in_progress_tasks, icon: '⚡', color: 'cyan' },
          { label: 'Performance', value: stats.performance_score, icon: '⭐', color: 'orange' },
        ].map((s, i) => (
          <div key={i} className={`stat-card accent-${s.color}`}>
            <div className="stat-card-header">
              <div>
                <div className="stat-card-label">{s.label}</div>
                <div className="stat-card-value">{s.value}</div>
              </div>
              <div className={`stat-card-icon ${s.color}`}>{s.icon}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid-2" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: '20px', fontWeight: 700, fontSize: '16px' }}>📊 My Task Status</h3>
          <div className="chart-container square">
            <Doughnut data={taskData} options={{ responsive: true, maintainAspectRatio: false, cutout: '65%',
              plugins: { legend: { labels: { color: 'rgba(255,255,255,0.7)', font: { size: 11 } } } } }} />
          </div>
        </div>
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: '20px', fontWeight: 700, fontSize: '16px' }}>😊 Sentiment Trend</h3>
          <div className="chart-container">
            <Line data={sentimentData} options={{ responsive: true, maintainAspectRatio: false,
              plugins: { legend: { display: false } },
              scales: {
                x: { ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { min: 0, max: 1, ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' } },
              }}} />
          </div>
        </div>
      </div>

      {/* My Tasks List */}
      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: '20px', fontWeight: 700, fontSize: '16px' }}>📋 My Tasks</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {tasks?.slice(0, 10).map(task => (
            <div key={task.id} className="task-card">
              <div className="task-card-header">
                <div className="task-card-title">{task.title}</div>
                <span className={`badge badge-${statusColor[task.status] || 'neutral'}`}>
                  {task.status?.replace('_', ' ')}
                </span>
              </div>
              <div className="task-card-meta">
                <span className="task-card-meta-item">
                  📁 {task.project_name || 'Unknown Project'}
                </span>
                <span className="task-card-meta-item">
                  📅 {task.deadline || 'No deadline'}
                </span>
                <span className={`badge badge-${priorityColor[task.priority] || 'neutral'}`} style={{ fontSize: '10px' }}>
                  {task.priority}
                </span>
              </div>
            </div>
          ))}
          {(!tasks || tasks.length === 0) && (
            <div className="empty-state" style={{ padding: '40px' }}>
              <div className="empty-state-icon">✅</div>
              <div className="empty-state-title">No tasks assigned</div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
