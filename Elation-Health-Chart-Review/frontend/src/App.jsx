import { useState, useEffect } from 'react'
import Dashboard from './pages/Dashboard'
import QuickView from './pages/QuickView'
import Login from './pages/Login'
import { getAuthState, clearToken, setUnauthorizedCallback } from './api/client'
import './styles/app.css'

function App() {
  const [view, setView] = useState('dashboard') // 'dashboard' or patient MRN
  const [selectedPatientMRN, setSelectedPatientMRN] = useState(null)
  const [currentUser, setCurrentUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  // Initialize auth state on mount
  useEffect(() => {
    const auth = getAuthState()
    setCurrentUser(auth)
    setIsLoading(false)

    // Set callback for when token expires during a session
    setUnauthorizedCallback(() => {
      setCurrentUser(null)
      setView('login')
    })
  }, [])

  const handleSelectPatient = (mrn) => {
    setSelectedPatientMRN(mrn)
    setView('quickview')
  }

  const handleBackToDashboard = () => {
    setView('dashboard')
    setSelectedPatientMRN(null)
  }

  const handleLogin = (user) => {
    setCurrentUser(user)
    setView('dashboard')
  }

  const handleLogout = () => {
    clearToken()
    setCurrentUser(null)
    setView('login')
  }

  if (isLoading) {
    return <div className="app-loading">Loading...</div>
  }

  // Show login if not authenticated
  if (!currentUser) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>⚕️ Elation Health Chart Review</h1>
          <p className="subtitle">AI-Powered Pre-Visit Summaries</p>
        </div>
        <div className="header-right">
          <div className="user-info">
            <span className="user-role">{currentUser.role}</span>
            <span className="user-name">{currentUser.displayName}</span>
          </div>
          <button
            className={`view-button ${view === 'dashboard' ? 'active' : ''}`}
            onClick={handleBackToDashboard}
          >
            Dashboard
          </button>
          <button className="logout-button" onClick={handleLogout}>
            Log Out
          </button>
        </div>
      </header>

      <main className="app-main">
        {view === 'dashboard' ? (
          <Dashboard onSelectPatient={handleSelectPatient} />
        ) : (
          <QuickView
            mrn={selectedPatientMRN}
            onBack={handleBackToDashboard}
          />
        )}
      </main>
    </div>
  )
}

export default App
