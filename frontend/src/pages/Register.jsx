import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function Register() {
  const [form, setForm] = useState({
    full_name: '', email: '', password: '', role: 'employee', department: '', designation: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const user = await register(form)
      navigate(user.role === 'manager' ? '/dashboard' : '/my-dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  const update = (field, value) => setForm(prev => ({ ...prev, [field]: value }))

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-logo">
          <div className="auth-logo-icon">O</div>
          <div className="auth-logo-title">OrchestrAI</div>
          <div className="auth-logo-subtitle">Join TechNova Solutions</div>
        </div>
        <div className="auth-card">
          <h2 className="auth-title">Create Account</h2>
          {error && <div className="auth-error">{error}</div>}
          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <input id="reg-name" type="text" className="form-input" placeholder="John Doe"
                value={form.full_name} onChange={e => update('full_name', e.target.value)} required />
            </div>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input id="reg-email" type="email" className="form-input" placeholder="you@company.com"
                value={form.email} onChange={e => update('email', e.target.value)} required />
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <input id="reg-password" type="password" className="form-input" placeholder="••••••••"
                value={form.password} onChange={e => update('password', e.target.value)} required />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Role</label>
                <select id="reg-role" className="form-select" value={form.role}
                  onChange={e => update('role', e.target.value)}>
                  <option value="employee">Employee</option>
                  <option value="manager">Manager</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Department</label>
                <input type="text" className="form-input" placeholder="Engineering"
                  value={form.department} onChange={e => update('department', e.target.value)} />
              </div>
            </div>
            <button id="reg-submit" type="submit" className="btn btn-primary btn-lg" disabled={loading}
              style={{ width: '100%' }}>
              {loading ? '⏳ Creating...' : '✨ Create Account'}
            </button>
          </form>
          <div className="auth-footer">
            Already have an account? <Link to="/login">Sign in</Link>
          </div>
        </div>
      </div>
    </div>
  )
}
