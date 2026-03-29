import { useState, useRef, useEffect } from 'react'
import { JitsiMeeting } from '@jitsi/react-sdk'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function VideoConference() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [meetingState, setMeetingState] = useState('joining') // joining, active, wrapped
  const [roomName, setRoomName] = useState(`OrchestrAI-Meeting-${Math.floor(Math.random() * 100000)}`)
  const [transcript, setTranscript] = useState([])
  const [aiAnalysis, setAiAnalysis] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)
  
  // Realtime MOM Mock/Generator
  useEffect(() => {
    if (meetingState !== 'active') return
    
    // In a real production app, we would use window.SpeechRecognition here
    // For this demonstration, we'll simulate AI picking up conversation over time
    const snippets = [
      "📝 AI: Detecting project roadmap discussion...",
      "📝 AI: High priority task mentioned for deployment.",
      "📝 AI: Suggesting performance review for frontend team.",
      "📝 AI: Scheduling follow-up meeting for next week."
    ]
    let counter = 0
    const interval = setInterval(() => {
      setTranscript(prev => [...prev, snippets[counter % snippets.length]])
      counter++
    }, 15000)

    return () => clearInterval(interval)
  }, [meetingState])

  const handleMeetingEnd = async () => {
    setMeetingState('wrapped')
    setIsProcessing(true)
    
    try {
      // Send the accumulated transcript or metadata to backend
      const syntheticTranscript = `Meeting took place in room ${roomName}. Team discussed roadmap, frontend deployment (high priority), and scheduled a follow up for next week.`
      
      const form = {
        title: `Video Call: ${roomName}`,
        team_id: null,
        project_id: null,
        transcript: syntheticTranscript,
        duration_minutes: 30
      }
      
      const res = await api.post('/api/meetings', form)
      setAiAnalysis(res.data)
      
    } catch (err) {
      console.error("Error saving meeting:", err)
    } finally {
      setIsProcessing(false)
    }
  }

  if (meetingState === 'wrapped') {
    return (
      <div style={{ maxWidth: '800px', margin: '0 auto', paddingTop: '40px' }}>
         <div className="glass-card">
            <h2 style={{ marginBottom: '20px', color: 'var(--accent-green)' }}>✅ Meeting Finished</h2>
            
            {isProcessing ? (
              <div style={{ padding: '40px', textAlign: 'center' }}>
                <div className="loader-spinner" style={{ margin: '0 auto 20px auto' }} />
                <p>AI is generating Minutes of Meeting & extracting tasks...</p>
              </div>
            ) : aiAnalysis ? (
              <div>
                <div style={{ marginBottom: '20px', padding: '15px', background: 'rgba(0, 230, 118, 0.1)', borderRadius: '12px', border: '1px solid rgba(0, 230, 118, 0.2)' }}>
                  <h4>Generated Tasks</h4>
                  <p>{aiAnalysis.tasks_created} tasks were automatically created and assigned!</p>
                </div>
                
                <h3>Minutes of Meeting (MOM)</h3>
                <div className="meeting-summary" style={{ marginTop: '16px' }} dangerouslySetInnerHTML={{
                  __html: aiAnalysis.summary?.replace(/\n/g, '<br>').replace(/## (.*)/g, '<h2>$1</h2>').replace(/### (.*)/g, '<h3>$1</h3>').replace(/- (.*)/g, '<li>$1</li>')
                }} />
                
                <button className="btn btn-primary" style={{ marginTop: '30px' }} onClick={() => navigate('/meetings')}>
                  Back to Meeting Hub
                </button>
              </div>
            ) : (
              <p>Error generating analysis.</p>
            )}
         </div>
      </div>
    )
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 350px', height: 'calc(100vh - 100px)', gap: '20px' }}>
      {/* Jitsi Video Area */}
      <div style={{ borderRadius: '16px', overflow: 'hidden', border: '1px solid var(--glass-border)', background: '#000' }}>
        <JitsiMeeting
            domain="meet.jit.si"
            roomName={roomName}
            configOverwrite={{
                startWithAudioMuted: false,
                disableModeratorIndicator: true,
                startScreenSharing: false,
                enableEmailInStats: false
            }}
            interfaceConfigOverwrite={{
                DISABLE_JOIN_LEAVE_NOTIFICATIONS: true
            }}
            userInfo={{
                displayName: user?.full_name || 'Anonymous Employee'
            }}
            onApiReady={(externalApi) => {
              setMeetingState('active')
              
              externalApi.addListener('videoConferenceLeft', () => {
                handleMeetingEnd()
              })
            }}
            getIFrameRef={(iframeRef) => {
              iframeRef.style.height = '100%';
              iframeRef.style.width = '100%';
            }}
        />
      </div>

      {/* AI Live Sidebar */}
      <div className="glass-card no-hover" style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
        <div style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '16px', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="live-indicator" style={{ width: '8px', height: '8px', background: 'var(--accent-red)', borderRadius: '50%', display: 'inline-block', boxShadow: '0 0 8px var(--accent-red)' }} />
            AI Live Analysis
          </h3>
          <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
            OrchestrAI is listening and taking notes...
          </p>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {transcript.length === 0 && (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-tertiary)', fontSize: '13px' }}>
              Awaiting conversation...
            </div>
          )}
          
          {transcript.map((t, i) => (
            <div key={i} style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', borderLeft: '3px solid var(--accent-primary)', fontSize: '13px', lineHeight: 1.5, animation: 'scaleIn 0.3s ease-out' }}>
              {t}
            </div>
          ))}
        </div>
        
        <div style={{ paddingTop: '16px', borderTop: '1px solid var(--glass-border)', marginTop: 'auto' }}>
           <button className="btn btn-danger" style={{ width: '100%' }} onClick={handleMeetingEnd}>
             End Meeting & Generate MOM
           </button>
        </div>
      </div>
      
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes pulse-red {
          0% { box-shadow: 0 0 0 0 rgba(255, 82, 82, 0.7); }
          70% { box-shadow: 0 0 0 10px rgba(255, 82, 82, 0); }
          100% { box-shadow: 0 0 0 0 rgba(255, 82, 82, 0); }
        }
        .live-indicator { animation: pulse-red 2s infinite; }
      `}} />
    </div>
  )
}
