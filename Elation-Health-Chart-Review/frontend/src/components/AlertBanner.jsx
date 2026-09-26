import '../styles/components.css'

function AlertBanner({ alert }) {
  const severityIcon = {
    high: '🚨',
    medium: '⚠️',
    low: 'ℹ️'
  }

  return (
    <div className={`alert-banner alert-${alert.severity}`}>
      <span className="alert-icon">{severityIcon[alert.severity]}</span>
      <div className="alert-content">
        <strong>{alert.patientName}</strong> ({alert.patientMRN})
        <p>{alert.message}</p>
      </div>
    </div>
  )
}

export default AlertBanner
