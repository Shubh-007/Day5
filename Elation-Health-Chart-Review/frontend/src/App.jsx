import { useState, useEffect } from 'react'
import Dashboard from './pages/Dashboard'
import QuickView from './pages/QuickView'
import './styles/app.css'

function App() {
  const [view, setView] = useState('dashboard') // 'dashboard' or patient MRN
  const [selectedPatientMRN, setSelectedPatientMRN] = useState(null)

  const handleSelectPatient = (mrn) => {
    setSelectedPatientMRN(mrn)
    setView('quickview')
  }

  const handleBackToDashboard = () => {
    setView('dashboard')
    setSelectedPatientMRN(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>⚕️ Elation Health Chart Review</h1>
          <p className="subtitle">AI-Powered Pre-Visit Summaries</p>
        </div>
        <button
          className={`view-button ${view === 'dashboard' ? 'active' : ''}`}
          onClick={handleBackToDashboard}
        >
          Dashboard
        </button>
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
