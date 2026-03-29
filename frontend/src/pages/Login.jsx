import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('rahul.sharma@technova.com')
  const [password, setPassword] = useState('demo123')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const user = await login(email, password)
      navigate(user.role === 'manager' ? '/dashboard' : '/my-dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-logo">
          <div className="auth-logo-icon">O</div>
          <div className="auth-logo-title">OrchestrAI</div>
          <div className="auth-logo-subtitle">Autonomous Enterprise Workflow Management</div>
        </div>

        <div className="auth-card">
          <h2 className="auth-title">Welcome Back</h2>

          {error && <div className="auth-error">{error}</div>}

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Email Address</label>
              <input
                id="login-email"
                type="email"
                className="form-input"
                placeholder="you@company.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <input
                id="login-password"
                type="password"
                className="form-input"
                placeholder="••••••••"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
              />
            </div>
            <button id="login-submit" type="submit" className="btn btn-primary btn-lg" disabled={loading}
              style={{ width: '100%', marginTop: '8px' }}>
              {loading ? '⏳ Signing in...' : '🚀 Sign In'}
            </button>
          </form>

          <div className="auth-footer">
            Don't have an account? <Link to="/register">Create one</Link>
          </div>

          <div style={{
            marginTop: '24px', padding: '16px', background: 'rgba(102,126,234,0.08)',
            borderRadius: '12px', fontSize: '12px', color: 'var(--text-tertiary)',
          }}>
            <div style={{ fontWeight: 600, marginBottom: '8px', color: 'var(--accent-cyan)' }}>
              🔑 Demo Credentials
            </div>
            <div style={{ display: 'grid', gap: '4px' }}>
              <div><strong>Manager:</strong> rahul.sharma@technova.com / demo123</div>
              <div><strong>Employee:</strong> priya.patel@technova.com / demo123</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
