import { useState, useEffect } from 'react'
import api from '../services/api'

export default function MeetingInput() {
  const [teams, setTeams] = useState([])
  const [projects, setProjects] = useState([])
  const [meetings, setMeetings] = useState([])
  const [form, setForm] = useState({ title: '', team_id: '', project_id: '', transcript: '', duration_minutes: 60 })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  useEffect(() => { fetchData() }, [])

  const fetchData = async () => {
    try {
      const [t, p, m] = await Promise.all([api.get('/api/teams'), api.get('/api/projects'), api.get('/api/meetings')])
      setTeams(t.data)
      setProjects(p.data)
      setMeetings(m.data)
    } catch {}
  }

  const processMeeting = async (e) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)
    try {
      const res = await api.post('/api/meetings', form)
      setResult(res.data)
      setForm({ title: '', team_id: '', project_id: '', transcript: '', duration_minutes: 60 })
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error processing meeting')
    } finally { setLoading(false) }
  }

  const priorityColor = { low: 'neutral', medium: 'primary', high: 'warning', critical: 'danger' }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title"><span className="page-title-icon">🎙️</span> Meeting Hub</h1>
          <p className="page-subtitle">Input meeting transcripts and let AI extract tasks automatically</p>
        </div>
      </div>

      <div className="grid-2">
        {/* Meeting Input */}
        <div className="glass-card no-hover">
          <h3 style={{ fontWeight: 700, marginBottom: '20px', fontSize: '16px' }}>📝 New Meeting</h3>
          <form onSubmit={processMeeting} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div className="form-group">
              <label className="form-label">Meeting Title</label>
              <input className="form-input" placeholder="e.g. Sprint Planning" value={form.title}
                onChange={e => setForm({...form, title: e.target.value})} required />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Team</label>
                <select className="form-select" value={form.team_id} onChange={e => setForm({...form, team_id: e.target.value})}>
                  <option value="">Select team...</option>
                  {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Project</label>
                <select className="form-select" value={form.project_id} onChange={e => setForm({...form, project_id: e.target.value})}>
                  <option value="">Select project...</option>
                  {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                </select>
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Meeting Transcript / Notes</label>
              <textarea className="form-textarea" rows={10} placeholder="Paste your meeting transcript here... The AI will summarize it and extract tasks automatically."
                value={form.transcript} onChange={e => setForm({...form, transcript: e.target.value})} required
                style={{ minHeight: '200px' }} />
            </div>
            <button type="submit" className="btn btn-primary btn-lg" disabled={loading} style={{ width: '100%' }}>
              {loading ? '🤖 AI Processing...' : '🚀 Process Meeting with AI'}
            </button>
          </form>
        </div>

        {/* AI Results */}
        <div>
          {result ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div className="glass-card no-hover" style={{ borderColor: 'rgba(0,230,118,0.3)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                  <span style={{ fontSize: '20px' }}>✅</span>
                  <h3 style={{ fontWeight: 700, color: 'var(--accent-green)' }}>
                    {result.tasks_created} Tasks Created
                  </h3>
                </div>
                <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{result.message}</p>
              </div>

              <div className="glass-card no-hover">
                <h3 style={{ fontWeight: 700, marginBottom: '16px', fontSize: '16px' }}>📋 Meeting Summary</h3>
                <div className="meeting-summary" dangerouslySetInnerHTML={{
                  __html: result.summary?.replace(/\n/g, '<br>').replace(/## (.*)/g, '<h2>$1</h2>').replace(/### (.*)/g, '<h3>$1</h3>').replace(/- (.*)/g, '<li>$1</li>')
                }} />
              </div>

              <div className="glass-card no-hover">
                <h3 style={{ fontWeight: 700, marginBottom: '16px', fontSize: '16px' }}>📋 Extracted Tasks</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {result.tasks?.map((task, i) => (
                    <div key={i} className="task-card">
                      <div className="task-card-header">
                        <span className="task-card-title">{task.title}</span>
                        <span className={`badge badge-${priorityColor[task.priority]}`}>{task.priority}</span>
                      </div>
                      <div className="task-card-meta">
                        {task.assigned_to && <span>👤 {task.assigned_to}</span>}
                        {task.deadline && <span>📅 {task.deadline}</span>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div>
              <div className="glass-card no-hover" style={{ marginBottom: '20px' }}>
                <h3 style={{ fontWeight: 700, marginBottom: '16px' }}>🤖 How it Works</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px', color: 'var(--text-secondary)' }}>
                  {['Paste your meeting transcript', 'AI summarizes key points', 'AI extracts actionable tasks', 'AI assigns tasks to team members', 'AI sets smart deadlines', 'Tasks are stored & notifications sent'].map((step, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <div style={{
                        width: '28px', height: '28px', borderRadius: '50%', background: 'var(--accent-gradient)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '12px', flexShrink: 0,
                      }}>{i + 1}</div>
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent Meetings */}
              <div className="glass-card no-hover">
                <h3 style={{ fontWeight: 700, marginBottom: '16px' }}>📚 Recent Meetings</h3>
                {meetings.slice(0, 5).map(m => (
                  <div key={m.id} style={{
                    padding: '12px 0', borderBottom: '1px solid var(--glass-border)', fontSize: '13px',
                  }}>
                    <div style={{ fontWeight: 600 }}>{m.title}</div>
                    <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                      {m.meeting_date?.split('T')[0]} • {m.duration_minutes}min
                    </div>
                  </div>
                ))}
                {meetings.length === 0 && <p style={{ color: 'var(--text-tertiary)', fontSize: '13px' }}>No meetings yet. Process your first meeting above!</p>}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
