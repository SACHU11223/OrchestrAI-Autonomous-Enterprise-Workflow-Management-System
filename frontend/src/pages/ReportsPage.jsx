import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'

export default function ReportsPage() {
  const { user } = useAuth()
  const [reports, setReports] = useState([])
  const [teams, setTeams] = useState([])
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [selectedReport, setSelectedReport] = useState(null)
  const [form, setForm] = useState({ title: '', report_type: 'weekly', project_id: '', team_id: '', period_start: '', period_end: '' })

  useEffect(() => { fetchData() }, [])

  const fetchData = async () => {
    try {
      const [r, t, p] = await Promise.all([api.get('/api/reports'), api.get('/api/teams'), api.get('/api/projects')])
      setReports(r.data); setTeams(t.data); setProjects(p.data)
    } catch {} finally { setLoading(false) }
  }

  const generateReport = async (e) => {
    e.preventDefault()
    setGenerating(true)
    try {
      const res = await api.post('/api/reports', form)
      setShowModal(false)
      fetchData()
      setSelectedReport(res.data.report)
    } catch (err) { alert('Error generating report') }
    finally { setGenerating(false) }
  }

  const downloadPdf = async (reportId) => {
    try {
      const res = await api.get(`/api/reports/${reportId}/pdf`, { responseType: 'blob' })
      const url = URL.createObjectURL(new Blob([res.data]))
      const a = document.createElement('a'); a.href = url; a.download = `report.pdf`; a.click()
    } catch { alert('PDF download: install reportlab on backend') }
  }

  if (loading) return <div className="loader"><div className="loader-spinner" /></div>

  return (
    <div>
      <div className="page-header">
        <div><h1 className="page-title"><span className="page-title-icon">📄</span> Reports</h1>
        <p className="page-subtitle">AI-generated team and project reports</p></div>
        {user?.role === 'manager' && <button className="btn btn-primary" onClick={() => setShowModal(true)}>🤖 Generate Report</button>}
      </div>
      <div className="grid-2">
        <div className="glass-card no-hover">
          <h3 style={{ fontWeight: 700, marginBottom: 20 }}>📚 All Reports</h3>
          {reports.map(r => (
            <div key={r.id} className="task-card" style={{ cursor: 'pointer', marginBottom: 10 }} onClick={() => setSelectedReport(r.content || r)}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div><div style={{ fontWeight: 600, fontSize: 14 }}>{r.title}</div>
                  <div style={{ fontSize: 11, color: 'var(--text-tertiary)', marginTop: 4 }}>{r.period_start} → {r.period_end}</div></div>
                <div style={{ display: 'flex', gap: 6 }}>
                  <span className={`badge badge-${r.report_type==='weekly'?'primary':'info'}`}>{r.report_type}</span>
                  <button className="btn btn-ghost btn-sm" onClick={e => { e.stopPropagation(); downloadPdf(r.id) }}>📥</button>
                </div>
              </div>
              {r.summary && <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 8 }}>{r.summary.slice(0,150)}...</p>}
            </div>
          ))}
          {reports.length===0 && <div className="empty-state" style={{padding:40}}><div className="empty-state-icon">📄</div><div className="empty-state-title">No reports</div></div>}
        </div>
        <div className="glass-card no-hover">
          <h3 style={{ fontWeight: 700, marginBottom: 20 }}>📖 Preview</h3>
          {selectedReport ? (
            <div style={{ fontSize: 13, lineHeight: 1.8 }}>
              {selectedReport.title && <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16, color: 'var(--accent-cyan)' }}>{selectedReport.title}</h2>}
              {selectedReport.executive_summary && <><h4 style={{color:'var(--accent-primary)',marginBottom:8}}>Executive Summary</h4><p style={{color:'var(--text-secondary)'}}>{selectedReport.executive_summary}</p></>}
              {selectedReport.metrics && <div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:8,margin:'16px 0'}}>
                {Object.entries(selectedReport.metrics).map(([k,v])=><div key={k} style={{padding:10,background:'var(--glass-bg)',borderRadius:8}}>
                  <div style={{fontSize:10,color:'var(--text-tertiary)',textTransform:'uppercase'}}>{k.replace(/_/g,' ')}</div>
                  <div style={{fontSize:18,fontWeight:700,marginTop:2}}>{v}</div></div>)}</div>}
              {selectedReport.highlights?.map((h,i)=><div key={i} style={{padding:'4px 0',color:'var(--text-secondary)'}}>✨ {h}</div>)}
              {selectedReport.recommendations?.map((r,i)=><div key={i} style={{padding:'4px 0',color:'var(--text-secondary)'}}>💡 {r}</div>)}
            </div>
          ) : <div className="empty-state" style={{padding:60}}><div className="empty-state-icon">👈</div><div className="empty-state-title">Select a report</div></div>}
        </div>
      </div>
      {showModal && <div className="modal-overlay" onClick={()=>setShowModal(false)}>
        <div className="modal" onClick={e=>e.stopPropagation()}>
          <div className="modal-header"><h3 className="modal-title">Generate Report</h3><button className="modal-close" onClick={()=>setShowModal(false)}>×</button></div>
          <form onSubmit={generateReport}>
            <div className="modal-body" style={{display:'flex',flexDirection:'column',gap:16}}>
              <div className="form-group"><label className="form-label">Title</label><input className="form-input" value={form.title} onChange={e=>setForm({...form,title:e.target.value})} required /></div>
              <div className="form-group"><label className="form-label">Type</label><select className="form-select" value={form.report_type} onChange={e=>setForm({...form,report_type:e.target.value})}><option value="weekly">Weekly</option><option value="monthly">Monthly</option></select></div>
              <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16}}>
                <div className="form-group"><label className="form-label">Project</label><select className="form-select" value={form.project_id} onChange={e=>setForm({...form,project_id:e.target.value})}><option value="">All</option>{projects.map(p=><option key={p.id} value={p.id}>{p.name}</option>)}</select></div>
                <div className="form-group"><label className="form-label">Team</label><select className="form-select" value={form.team_id} onChange={e=>setForm({...form,team_id:e.target.value})}><option value="">All</option>{teams.map(t=><option key={t.id} value={t.id}>{t.name}</option>)}</select></div>
              </div>
            </div>
            <div className="modal-footer"><button type="button" className="btn btn-secondary" onClick={()=>setShowModal(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={generating}>{generating?'Generating...':'Generate'}</button></div>
          </form></div></div>}
    </div>
  )
}
