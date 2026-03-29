import { useState, useEffect } from 'react'
import api from '../services/api'

export default function TeamManagement() {
  const [teams, setTeams] = useState([])
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [showAddMember, setShowAddMember] = useState(null)
  const [form, setForm] = useState({ name: '', description: '', color: '#667eea' })

  useEffect(() => { fetchData() }, [])

  const fetchData = async () => {
    try {
      const [teamsRes, usersRes] = await Promise.all([api.get('/api/teams'), api.get('/api/auth/users')])
      setTeams(teamsRes.data)
      setUsers(usersRes.data.filter(u => u.role === 'employee'))
    } catch (err) { console.error(err) }
    finally { setLoading(false) }
  }

  const createTeam = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/teams', form)
      setShowModal(false)
      setForm({ name: '', description: '', color: '#667eea' })
      fetchData()
    } catch (err) { alert(err.response?.data?.detail || 'Error creating team') }
  }

  const addMember = async (userId) => {
    try {
      await api.post(`/api/teams/${showAddMember}/members`, { user_id: userId })
      setShowAddMember(null)
      fetchData()
    } catch (err) { alert(err.response?.data?.detail || 'Error adding member') }
  }

  const removeMember = async (teamId, userId) => {
    try {
      await api.delete(`/api/teams/${teamId}/members/${userId}`)
      fetchData()
    } catch (err) { alert('Error removing member') }
  }

  if (loading) return <div className="loader"><div className="loader-spinner" /></div>

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title"><span className="page-title-icon">👥</span> Team Management</h1>
          <p className="page-subtitle">Manage your teams and team members</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Create Team</button>
      </div>

      <div className="grid-cards">
        {teams.map(team => (
          <div key={team.id} className="glass-card" style={{ borderLeft: `3px solid ${team.color || '#667eea'}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
              <div>
                <h3 style={{ fontSize: '18px', fontWeight: 700 }}>{team.name}</h3>
                <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>{team.description}</p>
              </div>
              <span className="badge badge-primary">{team.member_count || 0} members</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '16px' }}>
              {team.members?.map(m => (
                <div key={m.id} style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  padding: '8px 12px', background: 'var(--glass-bg)', borderRadius: '10px',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{
                      width: '32px', height: '32px', borderRadius: '50%', background: team.color || 'var(--accent-gradient)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '12px',
                    }}>
                      {m.full_name?.charAt(0)}
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '13px' }}>{m.full_name}</div>
                      <div style={{ fontSize: '11px', color: 'var(--text-tertiary)' }}>{m.designation}</div>
                    </div>
                  </div>
                  <button className="btn btn-ghost btn-sm" onClick={() => removeMember(team.id, m.id)}
                    style={{ fontSize: '12px', color: 'var(--accent-red)' }}>✕</button>
                </div>
              ))}
            </div>

            <button className="btn btn-secondary btn-sm" onClick={() => setShowAddMember(team.id)}
              style={{ width: '100%' }}>+ Add Member</button>
          </div>
        ))}
      </div>

      {/* Create Team Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">Create New Team</h3>
              <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={createTeam}>
              <div className="modal-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div className="form-group">
                  <label className="form-label">Team Name</label>
                  <input className="form-input" placeholder="e.g. AI Team" value={form.name}
                    onChange={e => setForm({...form, name: e.target.value})} required />
                </div>
                <div className="form-group">
                  <label className="form-label">Description</label>
                  <textarea className="form-textarea" placeholder="What does this team do?"
                    value={form.description} onChange={e => setForm({...form, description: e.target.value})} />
                </div>
                <div className="form-group">
                  <label className="form-label">Team Color</label>
                  <input type="color" value={form.color} onChange={e => setForm({...form, color: e.target.value})}
                    style={{ width: '60px', height: '36px', border: 'none', background: 'transparent', cursor: 'pointer' }} />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Create Team</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Member Modal */}
      {showAddMember && (
        <div className="modal-overlay" onClick={() => setShowAddMember(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">Add Team Member</h3>
              <button className="modal-close" onClick={() => setShowAddMember(null)}>×</button>
            </div>
            <div className="modal-body">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {users.map(u => {
                  const team = teams.find(t => t.id === showAddMember)
                  const isMember = team?.members?.some(m => m.id === u.id)
                  return (
                    <div key={u.id} style={{
                      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                      padding: '10px 14px', background: 'var(--glass-bg)', borderRadius: '10px',
                      opacity: isMember ? 0.4 : 1,
                    }}>
                      <div>
                        <div style={{ fontWeight: 600, fontSize: '13px' }}>{u.full_name}</div>
                        <div style={{ fontSize: '11px', color: 'var(--text-tertiary)' }}>{u.department} • {u.designation}</div>
                      </div>
                      {!isMember && (
                        <button className="btn btn-primary btn-sm" onClick={() => addMember(u.id)}>Add</button>
                      )}
                      {isMember && <span className="badge badge-neutral">Already added</span>}
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
