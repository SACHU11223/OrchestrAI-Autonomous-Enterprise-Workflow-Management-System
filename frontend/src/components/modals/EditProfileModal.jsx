import { useState } from 'react'
import api from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'

export default function EditProfileModal({ onClose }) {
  const { user, login } = useAuth()
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    department: user?.department || '',
    designation: user?.designation || '',
    phone: user?.phone || '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const res = await api.put('/api/auth/profile', formData)
      
      // Update local storage and context
      const existingToken = localStorage.getItem('token')
      if (existingToken) {
          // Keep token, just update user object in context manually or force reconnect
          // Since our auth context logic uses token decoding, we might need to fetch /api/auth/me
          // For now, let's trigger a full page reload or update context manually if possible.
          window.location.reload()
      }
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      zIndex: 1000
    }}>
      <div className="card" style={{ width: '400px', animation: 'scaleIn 0.2s ease-out' }}>
        <h2 style={{ marginTop: 0, marginBottom: '20px' }}>Edit Profile</h2>
        {error && <div className="alert alert-error">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input 
              type="text" 
              name="full_name"
              className="form-control" 
              value={formData.full_name} 
              onChange={handleChange} 
              required 
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">Department</label>
            <input 
              type="text" 
              name="department"
              className="form-control" 
              value={formData.department} 
              onChange={handleChange} 
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">Designation</label>
            <input 
              type="text" 
              name="designation"
              className="form-control" 
              value={formData.designation} 
              onChange={handleChange} 
            />
          </div>

          <div className="form-group">
            <label className="form-label">Phone</label>
            <input 
              type="text" 
              name="phone"
              className="form-control" 
              value={formData.phone} 
              onChange={handleChange} 
            />
          </div>
          
          <div style={{ display: 'flex', gap: '10px', marginTop: '30px' }}>
            <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" style={{ flex: 1 }} disabled={loading}>
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
