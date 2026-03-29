import { createContext, useContext, useEffect, useState } from 'react'
import { useAuth } from './AuthContext'

const RealtimeContext = createContext({})

export const useRealtime = () => useContext(RealtimeContext)

export function RealtimeProvider({ children }) {
  const { user } = useAuth()
  const [ws, setWs] = useState(null)
  
  useEffect(() => {
    if (!user?.id) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.hostname === 'localhost' ? 'localhost:8000' : window.location.host
    const socket = new WebSocket(`${protocol}//${host}/api/ws/${user.id}`)

    socket.onopen = () => {
      console.log('🔗 Realtime sync connected')
      // Ping to keep alive
      const interval = setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
          socket.send('ping')
        }
      }, 30000)
      
      socket.intervalId = interval
    }

    socket.onmessage = (event) => {
      try {
        if (event.data === 'pong') return; // Ignore keepalives
        const data = JSON.parse(event.data)
        console.log('📡 Realtime update:', data)
        
        // Dispatch global CustomEvent for components to hook into
        window.dispatchEvent(new CustomEvent('orchestrai:sync', { detail: data }))
        
        // If it is a task update, let's trigger an event specifically for tasks
        if (data.type === 'NEW_TASK' || data.type === 'TASK_UPDATED') {
            window.dispatchEvent(new CustomEvent('orchestrai:task_updated', { detail: data }))
        }
      } catch (e) {
        console.error('Error parsing sync message:', e)
      }
    }

    socket.onclose = () => {
      console.log('🔗 Realtime sync disconnected')
      if (socket.intervalId) clearInterval(socket.intervalId)
    }

    setWs(socket)

    return () => {
      if (socket.intervalId) clearInterval(socket.intervalId)
      socket.close()
    }
  }, [user])

  return (
    <RealtimeContext.Provider value={{ ws }}>
      {children}
    </RealtimeContext.Provider>
  )
}
