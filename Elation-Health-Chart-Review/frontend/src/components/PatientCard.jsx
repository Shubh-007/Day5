import '../styles/components.css'

function PatientCard({ patient, onSelect }) {
  const hasHighAlerts = patient.alerts.some(a => a.severity === 'high')
  const hasAbnormalLabs = patient.abnormalLabs.length > 0

  return (
    <div className={`patient-card ${hasHighAlerts ? 'has-high-alert' : ''}`} onClick={onSelect}>
      <div className="card-header">
        <div>
          <h4>{patient.patientName}</h4>
          <p className="card-mrn">MRN: {patient.patientMRN}</p>
        </div>
        <span className={`visit-badge ${patient.nextVisitIn.includes('days overdue') ? 'overdue' : ''}`}>
          {patient.nextVisitIn}
        </span>
      </div>

      <div className="card-body">
        <p className="patient-demographics">{patient.age}y • {patient.gender}</p>

        <div className="conditions-section">
          <strong>Conditions:</strong> {patient.problemList}
        </div>

        {hasAbnormalLabs && (
          <div className="labs-warning">
            ⚠️ {patient.abnormalLabs.length} abnormal lab(s)
          </div>
        )}

        {patient.alerts.length > 0 && (
          <div className="alerts-count">
            {patient.alerts.filter(a => a.severity === 'high').length > 0 && (
              <span className="alert-high">🚨 {patient.alerts.filter(a => a.severity === 'high').length} critical</span>
            )}
            {patient.alerts.filter(a => a.severity === 'medium').length > 0 && (
              <span className="alert-medium">⚠️ {patient.alerts.filter(a => a.severity === 'medium').length} medium</span>
            )}
          </div>
        )}
      </div>

      <div className="card-footer">
        <span className="meds-count">💊 {patient.medicationCount} meds</span>
        <button className="view-btn" onClick={(e) => { e.stopPropagation(); onSelect(); }}>
          Quick View →
        </button>
      </div>
    </div>
  )
}

export default PatientCard
