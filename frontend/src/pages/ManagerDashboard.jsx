import { useState, useEffect } from 'react'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Filler } from 'chart.js'
import { Doughnut, Bar, Line } from 'react-chartjs-2'
import api from '../services/api'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Filler)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: 'rgba(255,255,255,0.7)', font: { family: 'Inter', size: 11 }, padding: 16 } },
  },
  scales: {
    x: { ticks: { color: 'rgba(255,255,255,0.5)', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.05)' } },
    y: { ticks: { color: 'rgba(255,255,255,0.5)', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.05)' } },
  },
}

export default function ManagerDashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboard()
    
    const handleSync = () => fetchDashboard()
    window.addEventListener('orchestrai:sync', handleSync)
    return () => window.removeEventListener('orchestrai:sync', handleSync)
  }, [])

  const fetchDashboard = async () => {
    try {
      const res = await api.get('/api/dashboard/manager')
      setData(res.data)
    } catch (err) {
      console.error('Dashboard error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="loader"><div className="loader-spinner" /></div>
  if (!data) return <div className="empty-state"><div className="empty-state-icon">📊</div><div className="empty-state-title">Unable to load dashboard</div></div>

  const { stats, charts, employee_performance, delay_alerts } = data
  const taskStatusData = {
    labels: ['Completed', 'In Progress', 'Pending', 'Delayed'],
    datasets: [{
      data: [charts.task_status.completed, charts.task_status.in_progress, charts.task_status.pending, charts.task_status.delayed],
      backgroundColor: ['#00e676', '#667eea', '#ff9100', '#ff5252'],
      borderWidth: 0,
      hoverOffset: 8,
    }],
  }

  const sentimentData = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [{
      data: [charts.sentiment_distribution.positive, charts.sentiment_distribution.neutral, charts.sentiment_distribution.negative],
      backgroundColor: ['#00e676', '#ffd740', '#ff5252'],
      borderWidth: 0,
      hoverOffset: 8,
    }],
  }

  const priorityData = {
    labels: ['Low', 'Medium', 'High', 'Critical'],
    datasets: [{
      label: 'Tasks',
      data: [charts.task_priority.low, charts.task_priority.medium, charts.task_priority.high, charts.task_priority.critical],
      backgroundColor: ['rgba(0,212,255,0.6)', 'rgba(102,126,234,0.6)', 'rgba(255,145,0,0.6)', 'rgba(255,82,82,0.6)'],
      borderRadius: 8,
      borderSkipped: false,
    }],
  }

  const projectProgressData = {
    labels: charts.project_progress.map(p => p.name.length > 20 ? p.name.slice(0, 20) + '...' : p.name),
    datasets: [{
      label: 'Progress %',
      data: charts.project_progress.map(p => p.progress),
      backgroundColor: 'rgba(102, 126, 234, 0.3)',
      borderColor: '#667eea',
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#667eea',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 5,
    }],
  }

  return (
    <div>
      {/* Stats Grid */}
      <div className="grid-stats">
        {[
          { label: 'Total Tasks', value: stats.total_tasks, icon: '📋', color: 'blue' },
          { label: 'Completed', value: stats.completed_tasks, icon: '✅', color: 'green' },
          { label: 'In Progress', value: stats.in_progress_tasks, icon: '⚡', color: 'cyan' },
          { label: 'Delayed', value: stats.delayed_tasks, icon: '⚠️', color: 'red' },
          { label: 'Active Projects', value: stats.active_projects, icon: '📁', color: 'purple' },
          { label: 'Completion Rate', value: `${stats.completion_rate}%`, icon: '🎯', color: 'green' },
          { label: 'Avg Performance', value: stats.average_performance.toFixed(0), icon: '⭐', color: 'orange' },
          { label: 'Total Employees', value: stats.total_employees, icon: '👥', color: 'blue' },
        ].map((s, i) => (
          <div key={i} className={`stat-card accent-${s.color}`} style={{ animationDelay: `${i * 0.05}s` }}>
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

      {/* Charts Row */}
      <div className="grid-2" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: '20px', fontWeight: 700, fontSize: '16px' }}>📊 Task Status Distribution</h3>
          <div className="chart-container square">
            <Doughnut data={taskStatusData} options={{ ...chartOptions, scales: undefined, cutout: '65%' }} />
          </div>
        </div>
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: '20px', fontWeight: 700, fontSize: '16px' }}>📈 Task Priority Breakdown</h3>
          <div className="chart-container">
            <Bar data={priorityData} options={chartOptions} />
          </div>
        </div>
      </div>

      <div className="grid-2" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: '20px', fontWeight: 700, fontSize: '16px' }}>📈 Project Progress</h3>
          <div className="chart-container">
            <Line data={projectProgressData} options={chartOptions} />
          </div>
        </div>
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: '20px', fontWeight: 700, fontSize: '16px' }}>😊 Team Sentiment</h3>
          <div className="chart-container square">
            <Doughnut data={sentimentData} options={{ ...chartOptions, scales: undefined, cutout: '65%' }} />
          </div>
        </div>
      </div>

      {/* Employee Performance Table */}
      <div className="glass-card no-hover" style={{ marginBottom: 'var(--space-8)' }}>
        <h3 style={{ marginBottom: '20px', fontWeight: 700, fontSize: '16px' }}>⭐ Employee Performance</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>Employee</th>
              <th>Department</th>
              <th>Performance</th>
              <th>Productivity</th>
              <th>Tasks</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {employee_performance?.map(emp => (
              <tr key={emp.id}>
                <td style={{ fontWeight: 600 }}>{emp.name}</td>
                <td style={{ color: 'var(--text-tertiary)' }}>{emp.department}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div className="progress-bar" style={{ width: '80px' }}>
                      <div className="progress-bar-fill" style={{ width: `${emp.performance_score}%` }} />
                    </div>
                    <span style={{ fontSize: '12px', fontWeight: 600 }}>{emp.performance_score}</span>
                  </div>
                </td>
                <td>
                  <span style={{ fontSize: '13px', fontWeight: 600 }}>{emp.productivity_score}</span>
                </td>
                <td style={{ fontSize: '12px', color: 'var(--text-tertiary)' }}>
                  {emp.tasks_completed}/{emp.tasks_total}
                </td>
                <td>
                  <span className={`badge ${emp.performance_score >= 80 ? 'badge-success' : emp.performance_score >= 60 ? 'badge-warning' : 'badge-danger'}`}>
                    {emp.performance_score >= 80 ? 'Excellent' : emp.performance_score >= 60 ? 'Good' : 'Needs Review'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Delay Alerts */}
      {delay_alerts?.length > 0 && (
        <div className="glass-card no-hover" style={{ borderColor: 'rgba(255,82,82,0.2)' }}>
          <h3 style={{ marginBottom: '16px', fontWeight: 700, fontSize: '16px', color: 'var(--accent-red)' }}>
            🚨 Delay Risk Alerts
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {delay_alerts.map(task => (
              <div key={task.id} style={{
                padding: '12px 16px', background: 'rgba(255,82,82,0.06)', borderRadius: '12px',
                border: '1px solid rgba(255,82,82,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              }}>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '13px' }}>{task.title}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginTop: '2px' }}>
                    Deadline: {task.deadline || 'TBD'} • Priority: {task.priority}
                  </div>
                </div>
                <span className="badge badge-danger" style={{ fontSize: '11px' }}>
                  {(task.delay_probability * 100).toFixed(0)}% Risk
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
