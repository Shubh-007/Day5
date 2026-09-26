import '../styles/components.css'

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Loading patient summaries...</p>
    </div>
  )
}

export default LoadingSpinner
