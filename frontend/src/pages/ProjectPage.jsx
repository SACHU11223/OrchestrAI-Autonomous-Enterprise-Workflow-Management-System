import { useState, useEffect } from 'react'
import api from '../services/api'

export default function ProjectPage() {
  const [projects, setProjects] = useState([])
  const [teams, setTeams] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ name: '', description: '', team_id: '', start_date: '', end_date: '' })

  useEffect(() => { fetchData() }, [])

  const fetchData = async () => {
    try {
      const [p, t] = await Promise.all([api.get('/api/projects'), api.get('/api/teams')])
      setProjects(p.data)
      setTeams(t.data)
    } catch {} finally { setLoading(false) }
  }

  const createProject = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/projects', form)
      setShowModal(false)
      setForm({ name: '', description: '', team_id: '', start_date: '', end_date: '' })
      fetchData()
    } catch (err) { alert(err.response?.data?.detail || 'Error') }
  }

  const statusColors = { planning: 'info', active: 'success', completed: 'primary', on_hold: 'warning' }

  if (loading) return <div className="loader"><div className="loader-spinner" /></div>

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title"><span className="page-title-icon">📁</span> Projects</h1>
          <p className="page-subtitle">Manage and track all project progress</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ New Project</button>
      </div>

      <div className="grid-cards">
        {projects.map(project => (
          <div key={project.id} className="glass-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
              <h3 style={{ fontWeight: 700, fontSize: '16px', flex: 1 }}>{project.name}</h3>
              <span className={`badge badge-${statusColors[project.status] || 'neutral'}`}>{project.status}</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginBottom: '16px', lineHeight: 1.5 }}>
              {project.description?.slice(0, 120)}{project.description?.length > 120 ? '...' : ''}
            </p>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: '12px' }}>
                <span style={{ color: 'var(--text-tertiary)' }}>Progress</span>
                <span style={{ fontWeight: 600 }}>{project.progress}%</span>
              </div>
              <div className="progress-bar">
                <div className="progress-bar-fill" style={{ width: `${project.progress}%` }} />
              </div>
            </div>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', fontSize: '11px', color: 'var(--text-tertiary)' }}>
              <span>👥 {project.team_name}</span>
              {project.task_stats && (
                <>
                  <span>✅ {project.task_stats.completed}/{project.task_stats.total} tasks</span>
                  {project.task_stats.delayed > 0 && (
                    <span style={{ color: 'var(--accent-red)' }}>⚠️ {project.task_stats.delayed} delayed</span>
                  )}
                </>
              )}
            </div>

            <div style={{ display: 'flex', gap: '8px', marginTop: '12px', paddingTop: '12px', borderTop: '1px solid var(--glass-border)', fontSize: '11px', color: 'var(--text-tertiary)' }}>
              <span>📅 {project.start_date || 'TBD'}</span>
              <span>→</span>
              <span>{project.end_date || 'TBD'}</span>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">Create Project</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={createProject}>
              <div className="modal-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div className="form-group">
                  <label className="form-label">Project Name</label>
                  <input className="form-input" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
                </div>
                <div className="form-group">
                  <label className="form-label">Description</label>
                  <textarea className="form-textarea" value={form.description} onChange={e => setForm({...form, description: e.target.value})} />
                </div>
                <div className="form-group">
                  <label className="form-label">Team</label>
                  <select className="form-select" value={form.team_id} onChange={e => setForm({...form, team_id: e.target.value})} required>
                    <option value="">Select team...</option>
                    {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                  </select>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div className="form-group">
                    <label className="form-label">Start Date</label>
                    <input type="date" className="form-input" value={form.start_date} onChange={e => setForm({...form, start_date: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">End Date</label>
                    <input type="date" className="form-input" value={form.end_date} onChange={e => setForm({...form, end_date: e.target.value})} />
                  </div>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Create Project</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
