import { useState, useEffect } from 'react'
import LoadingSpinner from '../components/LoadingSpinner'
import '../styles/quickview.css'

function QuickView({ mrn, onBack }) {
  const [summary, setSummary] = useState(null)
  const [details, setDetails] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [reviewTime, setReviewTime] = useState(null)

  useEffect(() => {
    fetchPatientData()
    // Start timer for review time
    const startTime = Date.now()
    const timer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000)
      setReviewTime(elapsed)
    }, 1000)

    return () => clearInterval(timer)
  }, [mrn])

  const fetchPatientData = async () => {
    try {
      setLoading(true)
      const [summRes, detailRes] = await Promise.all([
        fetch(`/api/patients/${mrn}/summary`),
        fetch(`/api/patients/${mrn}`)
      ])

      if (!summRes.ok || !detailRes.ok) throw new Error('Failed to fetch patient data')

      const summData = await summRes.json()
      const detailData = await detailRes.json()

      setSummary(summData)
      setDetails(detailData)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />
  if (error) return <div className="error-message">Error: {error}</div>
  if (!summary) return <div className="error-message">Patient not found</div>

  return (
    <div className="quickview">
      <button className="back-btn" onClick={onBack}>← Back to Dashboard</button>

      <div className="quickview-container">
        <div className="quickview-header">
          <div className="patient-info">
            <h2>{summary.patientName}</h2>
            <p className="patient-details">
              {summary.age} years • {summary.gender} • MRN: {summary.patientMRN}
            </p>
            <p className="provider">PCP: {summary.primaryCareProvider}</p>
          </div>
          <div className="visit-timing">
            <div className="timing-item">
              <span className="timing-label">Last Visit:</span>
              <span className="timing-value">{summary.timeSinceLastVisit}</span>
            </div>
            <div className="timing-item">
              <span className="timing-label">Next Visit:</span>
              <span className="timing-value">{summary.nextVisitIn}</span>
            </div>
            {reviewTime !== null && (
              <div className="timing-item">
                <span className="timing-label">Review Time:</span>
                <span className="timing-value">{reviewTime}s</span>
              </div>
            )}
          </div>
        </div>

        <div className="quickview-content">
          {/* Vitals Card */}
          {summary.vitals && (
            <section className="card vitals-card">
              <h3>📊 Current Vitals</h3>
              <div className="vitals-grid">
                <div className="vital">
                  <span className="vital-label">BP</span>
                  <span className="vital-value">{summary.vitals.bloodPressure}</span>
                </div>
                <div className="vital">
                  <span className="vital-label">HR</span>
                  <span className="vital-value">{summary.vitals.heartRate} bpm</span>
                </div>
                <div className="vital">
                  <span className="vital-label">Weight</span>
                  <span className="vital-value">{summary.vitals.weight} lbs</span>
                </div>
                <div className="vital">
                  <span className="vital-label">BMI</span>
                  <span className="vital-value">{summary.vitals.bmi}</span>
                </div>
              </div>
            </section>
          )}

          {/* Problems Card */}
          <section className="card problems-card">
            <h3>🏥 Active Problems</h3>
            <ul>
              {summary.activeConditions.map((condition, idx) => (
                <li key={idx}>{condition}</li>
              ))}
            </ul>
          </section>

          {/* Medications Card */}
          <section className="card medications-card">
            <h3>💊 Current Medications ({summary.medicationCount})</h3>
            <ul>
              {summary.currentMedications.map((med, idx) => (
                <li key={idx}>{med}</li>
              ))}
            </ul>
          </section>

          {/* Abnormal Labs Card */}
          {summary.abnormalLabs.length > 0 && (
            <section className="card labs-card abnormal">
              <h3>⚠️ Abnormal Labs</h3>
              <ul>
                {summary.abnormalLabs.map((lab, idx) => (
                  <li key={idx} className="abnormal-lab">{lab}</li>
                ))}
              </ul>
            </section>
          )}

          {/* Recent Changes Card */}
          {summary.recentChanges.length > 0 && (
            <section className="card changes-card">
              <h3>📝 Recent Changes</h3>
              <div className="changes-list">
                {summary.recentChanges.map((change, idx) => (
                  <p key={idx}>{change}</p>
                ))}
              </div>
            </section>
          )}

          {/* Alerts Card */}
          {summary.alerts.length > 0 && (
            <section className="card alerts-card">
              <h3>🚨 Important Alerts</h3>
              <ul>
                {summary.alerts.map((alert, idx) => (
                  <li key={idx} className={`alert-${alert.severity}`}>
                    <strong>{alert.type}:</strong> {alert.message}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Allergies Section */}
          {details.allergies && details.allergies.length > 0 && (
            <section className="card allergies-card">
              <h3>🚫 Allergies</h3>
              <ul>
                {details.allergies.map((allergy, idx) => (
                  <li key={idx}>
                    <strong>{allergy.allergen}</strong> - {allergy.reactionType} ({allergy.severity})
                  </li>
                ))}
              </ul>
            </section>
          )}
        </div>

        <div className="quickview-footer">
          <p className="tip">💡 Tip: Review this summary in under 30 seconds before entering the exam room</p>
          <button className="action-btn" onClick={onBack}>Open Full Chart</button>
        </div>
      </div>
    </div>
  )
}

export default QuickView
