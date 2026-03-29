import { useState, useEffect } from 'react'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Filler, RadialLinearScale } from 'chart.js'
import { Bar, Doughnut, Radar } from 'react-chartjs-2'
import api from '../services/api'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Filler, RadialLinearScale)

export default function AnalyticsDashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchAnalytics() }, [])

  const fetchAnalytics = async () => {
    try {
      const res = await api.get('/api/dashboard/analytics')
      setData(res.data)
    } catch (err) { console.error(err) }
    finally { setLoading(false) }
  }

  if (loading) return <div className="loader"><div className="loader-spinner" /></div>
  if (!data) return <div className="empty-state"><div className="empty-state-icon">📈</div><div className="empty-state-title">No analytics data</div></div>

  const { team_tasks, team_performance, project_risks, total_metrics } = data

  const teamNames = Object.keys(team_tasks || {})
  const teamTaskData = {
    labels: teamNames,
    datasets: [
      { label: 'Completed', data: teamNames.map(t => team_tasks[t]?.completed || 0), backgroundColor: 'rgba(0,230,118,0.7)', borderRadius: 6, borderSkipped: false },
      { label: 'Total', data: teamNames.map(t => team_tasks[t]?.total || 0), backgroundColor: 'rgba(102,126,234,0.5)', borderRadius: 6, borderSkipped: false },
      { label: 'Delayed', data: teamNames.map(t => team_tasks[t]?.delayed || 0), backgroundColor: 'rgba(255,82,82,0.7)', borderRadius: 6, borderSkipped: false },
    ],
  }

  const perfNames = Object.keys(team_performance || {})
  const teamPerfData = {
    labels: perfNames,
    datasets: [{
      label: 'Avg Performance',
      data: perfNames.map(t => team_performance[t]?.avg_performance || 0),
      backgroundColor: perfNames.map(t => (team_performance[t]?.color || '#667eea') + '99'),
      borderColor: perfNames.map(t => team_performance[t]?.color || '#667eea'),
      borderWidth: 2, borderRadius: 8, borderSkipped: false,
    }],
  }

  const riskData = {
    labels: (project_risks || []).map(p => p.name?.length > 18 ? p.name.slice(0,18)+'...' : p.name),
    datasets: [
      { label: 'Risk Score', data: (project_risks || []).map(p => p.risk_score), backgroundColor: 'rgba(255,82,82,0.3)', borderColor: '#ff5252', pointBackgroundColor: '#ff5252' },
      { label: 'Progress', data: (project_risks || []).map(p => p.progress), backgroundColor: 'rgba(0,230,118,0.3)', borderColor: '#00e676', pointBackgroundColor: '#00e676' },
    ],
  }

  const opts = {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { labels: { color: 'rgba(255,255,255,0.7)', font: { family: 'Inter', size: 11 } } } },
    scales: {
      x: { ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' } },
      y: { ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' } },
    },
  }

  const radarOpts = {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { labels: { color: 'rgba(255,255,255,0.7)', font: { size: 11 } } } },
    scales: { r: { angleLines: { color: 'rgba(255,255,255,0.1)' }, grid: { color: 'rgba(255,255,255,0.08)' }, pointLabels: { color: 'rgba(255,255,255,0.6)', font: { size: 10 } }, ticks: { display: false }, suggestedMin: 0, suggestedMax: 100 } },
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title"><span className="page-title-icon">📈</span> Analytics Dashboard</h1>
          <p className="page-subtitle">Deep insights into team performance, risks, and productivity</p>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid-stats" style={{ marginBottom: 'var(--space-8)' }}>
        {[
          { label: 'Total Tasks', value: total_metrics?.total_tasks || 0, icon: '📋', color: 'blue' },
          { label: 'Completed', value: total_metrics?.total_completed || 0, icon: '✅', color: 'green' },
          { label: 'Total Feedback', value: total_metrics?.total_feedback || 0, icon: '💬', color: 'cyan' },
          { label: 'Avg Sentiment', value: ((total_metrics?.avg_sentiment || 0) * 100).toFixed(0) + '%', icon: '😊', color: 'purple' },
        ].map((s, i) => (
          <div key={i} className={`stat-card accent-${s.color}`}>
            <div className="stat-card-header">
              <div><div className="stat-card-label">{s.label}</div><div className="stat-card-value">{s.value}</div></div>
              <div className={`stat-card-icon ${s.color}`}>{s.icon}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Row 1 */}
      <div className="grid-2" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="glass-card no-hover">
          <h3 style={{ fontWeight: 700, marginBottom: 20, fontSize: 16 }}>👥 Team Task Distribution</h3>
          <div className="chart-container"><Bar data={teamTaskData} options={opts} /></div>
        </div>
        <div className="glass-card no-hover">
          <h3 style={{ fontWeight: 700, marginBottom: 20, fontSize: 16 }}>⭐ Team Performance Scores</h3>
          <div className="chart-container"><Bar data={teamPerfData} options={opts} /></div>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid-2" style={{ marginBottom: 'var(--space-8)' }}>
        <div className="glass-card no-hover">
          <h3 style={{ fontWeight: 700, marginBottom: 20, fontSize: 16 }}>📊 Project Risk vs Progress</h3>
          <div className="chart-container"><Radar data={riskData} options={radarOpts} /></div>
        </div>
        <div className="glass-card no-hover">
          <h3 style={{ fontWeight: 700, marginBottom: 20, fontSize: 16 }}>🏢 Team Overview</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {perfNames.map(name => {
              const tp = team_performance[name]
              const tt = team_tasks[name]
              return (
                <div key={name} style={{ padding: '16px', background: 'var(--glass-bg)', borderRadius: 12, borderLeft: `3px solid ${tp?.color || '#667eea'}` }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                    <div style={{ fontWeight: 700, fontSize: 14 }}>{name}</div>
                    <span className="badge badge-primary">{tp?.member_count || 0} members</span>
                  </div>
                  <div style={{ display: 'flex', gap: 16, fontSize: 12, color: 'var(--text-secondary)' }}>
                    <span>⭐ Perf: <strong>{tp?.avg_performance || 0}</strong></span>
                    <span>📋 Tasks: <strong>{tt?.total || 0}</strong></span>
                    <span>✅ Done: <strong>{tt?.completed || 0}</strong></span>
                    {(tt?.delayed || 0) > 0 && <span style={{ color: 'var(--accent-red)' }}>⚠️ Delayed: <strong>{tt.delayed}</strong></span>}
                  </div>
                  <div className="progress-bar" style={{ marginTop: 10 }}>
                    <div className="progress-bar-fill" style={{ width: `${tt?.total ? (tt.completed/tt.total*100) : 0}%`, background: tp?.color || 'var(--accent-gradient)' }} />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Project Risk Table */}
      <div className="glass-card no-hover">
        <h3 style={{ fontWeight: 700, marginBottom: 20, fontSize: 16 }}>🚨 Project Risk Assessment</h3>
        <table className="data-table">
          <thead><tr><th>Project</th><th>Progress</th><th>Risk Score</th><th>Status</th></tr></thead>
          <tbody>
            {(project_risks || []).map((p, i) => (
              <tr key={i}>
                <td style={{ fontWeight: 600 }}>{p.name}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <div className="progress-bar" style={{ width: 100 }}><div className="progress-bar-fill" style={{ width: `${p.progress}%` }} /></div>
                    <span style={{ fontSize: 12, fontWeight: 600 }}>{p.progress}%</span>
                  </div>
                </td>
                <td><span style={{ fontWeight: 700, color: p.risk_score >= 50 ? 'var(--accent-red)' : p.risk_score >= 25 ? 'var(--accent-orange)' : 'var(--accent-green)' }}>{p.risk_score}</span></td>
                <td><span className={`badge badge-${p.risk_score >= 50 ? 'danger' : p.risk_score >= 25 ? 'warning' : 'success'}`}>{p.risk_score >= 50 ? 'High Risk' : p.risk_score >= 25 ? 'Medium' : 'Low Risk'}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
