import { useState, useEffect } from 'react'
import axios from 'axios'
import { Shield, Activity, Globe, User, Clock, Terminal } from 'lucide-react'
import './App.css'

interface LogEntry {
  id: number
  timestamp: string
  ip_address: string
  port: number
  protocol: string
  username: string
  password: string
  city: string
  country: string
}

interface Stats {
  total_attacks: number
  unique_ips: number
  banned_count: number
}

function App() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [stats, setStats] = useState<Stats>({ total_attacks: 0, unique_ips: 0, banned_count: 0 })
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    try {
      const [logsRes, statsRes] = await Promise.all([
        axios.get('http://localhost:8000/api/logs'),
        axios.get('http://localhost:8000/api/stats')
      ])
      setLogs(logsRes.data)
      setStats(statsRes.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="dashboard-container">
      <header className="header">
        <div className="title-container">
          <h1 className="title glow">HoneyPot Sentinel</h1>
          <p style={{ margin: 0, opacity: 0.6 }}>Real-time Attack Pattern Detection</p>
        </div>
        <div className="status-badge" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div className="pulse" style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#4dff88' }}></div>
          <span style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>SYSTEM ACTIVE</span>
        </div>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <Activity size={24} color="#00f2ff" />
          <div className="stat-value">{stats.total_attacks}</div>
          <div className="stat-label">Total Connection Attempts</div>
        </div>
        <div className="stat-card">
          <Globe size={24} color="#00f2ff" />
          <div className="stat-value">{stats.unique_ips}</div>
          <div className="stat-label">Unique Attacker IPs</div>
        </div>
        <div className="stat-card">
          <Shield size={24} color="#ff4d4d" />
          <div className="stat-value">{stats.banned_count}</div>
          <div className="stat-label">Threats Blocked</div>
        </div>
        <div className="stat-card">
          <Terminal size={24} color="#00f2ff" />
          <div className="stat-value">{logs.length}</div>
          <div className="stat-label">Recent Vectors</div>
        </div>
      </div>

      <div className="main-content">
        <div className="card">
          <h2 className="card-title">Live Attack Feed</h2>
          <div style={{ overflowX: 'auto' }}>
            <table className="log-table">
              <thead>
                <tr>
                  <th>TIME</th>
                  <th>IP ADDRESS</th>
                  <th>PROTO</th>
                  <th>USERNAME</th>
                  <th>LOCATION</th>
                </tr>
              </thead>
              <tbody>
                {logs.map(log => (
                  <tr key={log.id}>
                    <td>{new Date(log.timestamp).toLocaleTimeString()}</td>
                    <td style={{ fontWeight: 'bold' }}>{log.ip_address}</td>
                    <td>
                      <span className={`protocol-tag ${log.protocol.toLowerCase()}-tag`}>
                        {log.protocol}
                      </span>
                    </td>
                    <td>{log.username || '---'}</td>
                    <td>{log.city}, {log.country}</td>
                  </tr>
                ))}
                {logs.length === 0 && !loading && (
                  <tr>
                    <td colSpan={5} style={{ textAlign: 'center', padding: '2rem', opacity: 0.5 }}>
                      Waiting for incoming traffic...
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <h2 className="card-title">Threat Intelligence</h2>
          <div className="map-placeholder">
            <Globe size={64} style={{ marginBottom: '1rem', opacity: 0.2 }} />
            <p style={{ opacity: 0.5 }}>Attacker Geolocation Visualization</p>
            <div style={{ width: '100%', padding: '1rem' }}>
               {logs.slice(0, 5).map(log => (
                 <div key={log.id} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.8rem' }}>
                    <span>{log.ip_address}</span>
                    <span style={{ color: 'var(--accent-color)' }}>{log.city}, {log.country}</span>
                 </div>
               ))}
            </div>
          </div>
          
          <div style={{ marginTop: '2rem' }}>
            <h3 style={{ fontSize: '1rem', marginBottom: '1rem' }}>Top Targeted Services</h3>
            <div style={{ background: 'rgba(255,255,255,0.05)', height: '20px', borderRadius: '10px', overflow: 'hidden', display: 'flex' }}>
              <div style={{ 
                width: `${(logs.filter(l => l.protocol === 'SSH').length / (logs.length || 1)) * 100}%`, 
                background: '#5c6bc0' 
              }}></div>
              <div style={{ 
                width: `${(logs.filter(l => l.protocol === 'FTP').length / (logs.length || 1)) * 100}%`, 
                background: '#ffa726' 
              }}></div>
            </div>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem', fontSize: '0.75rem' }}>
               <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><div style={{ width: 8, height: 8, background: '#5c6bc0' }}></div> SSH</span>
               <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><div style={{ width: 8, height: 8, background: '#ffa726' }}></div> FTP</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
