import { useState, useEffect } from 'react'
import PatientCard from '../components/PatientCard'
import AlertBanner from '../components/AlertBanner'
import LoadingSpinner from '../components/LoadingSpinner'
import { apiFetch } from '../api/client'
import '../styles/dashboard.css'

function Dashboard({ onSelectPatient }) {
  const [patients, setPatients] = useState([])
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDashboard()
  }, [])

  const fetchDashboard = async () => {
    try {
      setLoading(true)
      const [dashRes, alertsRes] = await Promise.all([
        apiFetch('/api/dashboard'),
        apiFetch('/api/alerts')
      ])

      const dashData = await dashRes.json()
      const alertsData = await alertsRes.json()

      setPatients(dashData.patients)
      setAlerts(alertsData.alerts)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />
  if (error) return <div className="error-message">Error: {error}</div>

  const criticalAlerts = alerts.filter(a => a.severity === 'high')

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="header-stats">
          <div className="stat">
            <span className="stat-value">{patients.length}</span>
            <span className="stat-label">Patients Today</span>
          </div>
          <div className="stat">
            <span className="stat-value">{alerts.length}</span>
            <span className="stat-label">Alerts</span>
          </div>
          <div className="stat critical">
            <span className="stat-value">{criticalAlerts.length}</span>
            <span className="stat-label">Critical</span>
          </div>
        </div>
        <button className="refresh-btn" onClick={fetchDashboard}>
          🔄 Refresh
        </button>
      </div>

      {criticalAlerts.length > 0 && (
        <div className="alerts-section">
          <h3>⚠️ Critical Alerts</h3>
          {criticalAlerts.map((alert, idx) => (
            <AlertBanner key={idx} alert={alert} />
          ))}
        </div>
      )}

      <div className="patients-grid">
        <h3>Patient Schedule</h3>
        <div className="patient-list">
          {patients.map((patient) => (
            <PatientCard
              key={patient.patientMRN}
              patient={patient}
              onSelect={() => onSelectPatient(patient.patientMRN)}
            />
          ))}
        </div>
      </div>

      <div className="dashboard-footer">
        <p>Last updated: {new Date().toLocaleTimeString()}</p>
      </div>
    </div>
  )
}

export default Dashboard
