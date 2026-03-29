import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'

export default function FeedbackPage() {
  const { user } = useAuth()
  const [feedbackList, setFeedbackList] = useState([])
  const [tasks, setTasks] = useState([])
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState(null)
  const [form, setForm] = useState({ content: '', task_id: '', project_id: '' })

  useEffect(() => { fetchData() }, [])

  const fetchData = async () => {
    try {
      const [f, t, p] = await Promise.all([
        api.get('/api/feedback'), api.get(user?.role === 'manager' ? '/api/tasks' : '/api/tasks/my'), api.get('/api/projects'),
      ])
      setFeedbackList(f.data)
      setTasks(t.data)
      setProjects(p.data)
    } catch {} finally { setLoading(false) }
  }

  const submitFeedback = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setResult(null)
    try {
      const res = await api.post('/api/feedback', form)
      setResult(res.data)
      setForm({ content: '', task_id: '', project_id: '' })
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error submitting feedback')
    } finally { setSubmitting(false) }
  }

  const sentimentEmoji = { positive: '😊', neutral: '😐', negative: '😟' }
  const sentimentColor = { positive: 'success', neutral: 'warning', negative: 'danger' }

  if (loading) return <div className="loader"><div className="loader-spinner" /></div>

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title"><span className="page-title-icon">💬</span> Daily Feedback</h1>
          <p className="page-subtitle">Submit your daily update and get AI-powered insights</p>
        </div>
      </div>

      <div className="grid-2">
        {/* Submit Feedback */}
        <div>
          <div className="glass-card no-hover">
            <h3 style={{ fontWeight: 700, marginBottom: '20px' }}>📝 Submit Daily Update</h3>
            <form onSubmit={submitFeedback} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Related Task</label>
                <select className="form-select" value={form.task_id} onChange={e => setForm({...form, task_id: e.target.value})}>
                  <option value="">Select task (optional)</option>
                  {tasks.filter(t => t.status !== 'completed').map(t => (
                    <option key={t.id} value={t.id}>{t.title}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Related Project</label>
                <select className="form-select" value={form.project_id} onChange={e => setForm({...form, project_id: e.target.value})}>
                  <option value="">Select project (optional)</option>
                  {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Your Update</label>
                <textarea className="form-textarea" rows={6} placeholder="How was your day? Share your progress, blockers, and feelings..."
                  value={form.content} onChange={e => setForm({...form, content: e.target.value})} required
                  style={{ minHeight: '150px' }} />
              </div>
              <button type="submit" className="btn btn-primary btn-lg" disabled={submitting} style={{ width: '100%' }}>
                {submitting ? '🤖 AI Analyzing...' : '📤 Submit & Analyze'}
              </button>
            </form>
          </div>

          {/* AI Result */}
          {result && (
            <div className="glass-card no-hover" style={{ marginTop: '20px', borderColor: 'rgba(0,212,255,0.2)' }}>
              <h3 style={{ fontWeight: 700, marginBottom: '16px', color: 'var(--accent-cyan)' }}>🤖 AI Analysis</h3>
              
              <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
                <div style={{ flex: 1, padding: '16px', background: 'var(--glass-bg)', borderRadius: '12px', textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', marginBottom: '4px' }}>{sentimentEmoji[result.sentiment?.sentiment] || '😐'}</div>
                  <div style={{ fontSize: '12px', fontWeight: 600, textTransform: 'capitalize' }}>{result.sentiment?.sentiment}</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-tertiary)' }}>Score: {(result.sentiment?.score * 100)?.toFixed(0)}%</div>
                </div>
                <div style={{ flex: 1, padding: '16px', background: 'var(--glass-bg)', borderRadius: '12px', textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', marginBottom: '4px' }}>
                    {result.delay_prediction?.risk_level === 'critical' ? '🚨' : result.delay_prediction?.risk_level === 'high' ? '⚠️' : '✅'}
                  </div>
                  <div style={{ fontSize: '12px', fontWeight: 600 }}>Delay Risk</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-tertiary)' }}>
                    {(result.delay_prediction?.delay_probability * 100)?.toFixed(0)}% probability
                  </div>
                </div>
              </div>

              {result.sentiment?.recommendation && (
                <div style={{ padding: '12px 16px', background: 'rgba(102,126,234,0.08)', borderRadius: '10px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                  💡 <strong>Recommendation:</strong> {result.sentiment.recommendation}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Feedback History */}
        <div className="glass-card no-hover">
          <h3 style={{ fontWeight: 700, marginBottom: '20px' }}>📚 Feedback History</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {feedbackList.slice(0, 15).map(f => (
              <div key={f.id} style={{
                padding: '14px 16px', background: 'var(--glass-bg)', borderRadius: '12px',
                borderLeft: `3px solid ${f.sentiment === 'positive' ? 'var(--accent-green)' : f.sentiment === 'negative' ? 'var(--accent-red)' : 'var(--accent-orange)'}`,
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <span style={{ fontWeight: 600, fontSize: '13px' }}>{f.user?.full_name || 'Employee'}</span>
                  <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                    <span style={{ fontSize: '16px' }}>{sentimentEmoji[f.sentiment] || '😐'}</span>
                    <span className={`badge badge-${sentimentColor[f.sentiment] || 'neutral'}`}>{f.sentiment}</span>
                  </div>
                </div>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  {f.content?.slice(0, 200)}{f.content?.length > 200 ? '...' : ''}
                </p>
                <div style={{ fontSize: '10px', color: 'var(--text-tertiary)', marginTop: '6px' }}>{f.feedback_date}</div>
              </div>
            ))}
            {feedbackList.length === 0 && (
              <div className="empty-state" style={{ padding: '40px' }}>
                <div className="empty-state-icon">💬</div>
                <div className="empty-state-title">No feedback yet</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
