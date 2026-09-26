import { useState, useEffect } from 'react'
import LoadingSpinner from '../components/LoadingSpinner'
import RAGChatbot from '../components/RAGChatbot'
import { apiFetch } from '../api/client'
import '../styles/quickview.css'

function QuickView({ mrn, onBack }) {
  const [summary, setSummary] = useState(null)
  const [details, setDetails] = useState(null)
  const [ragData, setRagData] = useState(null)
  const [drugInteractions, setDrugInteractions] = useState(null)
  const [clinicalGuidelines, setClinicalGuidelines] = useState(null)
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
      const [summRes, detailRes, ragRes] = await Promise.all([
        apiFetch(`/api/patients/${mrn}/summary`),
        apiFetch(`/api/patients/${mrn}`),
        apiFetch(`/api/tools/clinical-context/${mrn}?include=problems,medications,alerts`)
      ])

      const summData = await summRes.json()
      const detailData = await detailRes.json()
      const ragData = await ragRes.json()

      setSummary(summData)
      setDetails(detailData)
      if (ragData) {
        setRagData(ragData)
        await fetchDrugInteractions(summData.currentMedications)
        await fetchClinicalGuidelines(summData.activeConditions)
      }
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchDrugInteractions = async (medications) => {
    try {
      const drugNames = medications.map(m => m.split(' ')[0]) // Extract drug names
      const res = await apiFetch('/api/tools/drug-interactions', {
        method: 'POST',
        body: JSON.stringify({ medications: drugNames })
      })
      const data = await res.json()
      setDrugInteractions(data)
    } catch (err) {
      console.error('Failed to fetch drug interactions:', err)
    }
  }

  const fetchClinicalGuidelines = async (conditions) => {
    try {
      // Fetch guidelines for each condition
      const guidelines = {}
      for (const condition of conditions) {
        const res = await apiFetch(`/api/tools/retrieve/context?query=${encodeURIComponent(condition + ' management')}&context_type=guideline`)
        const data = await res.json()
        guidelines[condition] = data
      }
      setClinicalGuidelines(guidelines)
    } catch (err) {
      console.error('Failed to fetch clinical guidelines:', err)
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

          {/* RAG: Drug Safety Card */}
          {drugInteractions && drugInteractions.total_interactions > 0 && (
            <section className="card rag-card drug-safety">
              <h3>🔬 Drug Safety Check (RAG)</h3>
              <div className="rag-content">
                <p className="rag-metric">
                  <strong>{drugInteractions.total_interactions}</strong> interaction(s) detected
                </p>
                {drugInteractions.interactions && drugInteractions.interactions.length > 0 && (
                  <ul>
                    {drugInteractions.interactions.slice(0, 3).map((interaction, idx) => (
                      <li key={idx} className={`interaction-${interaction.severity || 'moderate'}`}>
                        <strong>{interaction.drug1}</strong> + <strong>{interaction.drug2}</strong>
                        {interaction.severity && <span className="severity-badge">{interaction.severity}</span>}
                        <p>{interaction.interaction_type}</p>
                      </li>
                    ))}
                  </ul>
                )}
                <p className="rag-source">🤖 Powered by RAG Clinical Database</p>
              </div>
            </section>
          )}

          {/* RAG: Clinical Guidelines Card */}
          {clinicalGuidelines && Object.keys(clinicalGuidelines).length > 0 && (
            <section className="card rag-card clinical-guidelines">
              <h3>📚 Clinical Guidelines (RAG)</h3>
              <div className="rag-content">
                {Object.entries(clinicalGuidelines).map(([condition, guidelines]) => (
                  <div key={condition} className="guideline-item">
                    <h4>{condition}</h4>
                    {guidelines.results && guidelines.results.length > 0 && (
                      <div className="guideline-summary">
                        <p>{guidelines.results[0].content?.substring(0, 150)}...</p>
                        {guidelines.results[0].relevance_score && (
                          <p className="relevance">
                            Relevance: <strong>{(guidelines.results[0].relevance_score * 100).toFixed(0)}%</strong>
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                ))}
                <p className="rag-source">🤖 Powered by RAG Clinical Database</p>
              </div>
            </section>
          )}

          {/* RAG: Clinical Context Card */}
          {ragData && ragData.retrieved_at && (
            <section className="card rag-card clinical-context">
              <h3>🧠 Clinical Context (RAG)</h3>
              <div className="rag-content">
                {ragData.problems && ragData.problems.length > 0 && (
                  <div className="context-section">
                    <h4>Problem List Summary</h4>
                    <ul>
                      {ragData.problems.slice(0, 3).map((p, idx) => (
                        <li key={idx}>{p.diagnosis} - {p.status}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {ragData.recent_labs && ragData.recent_labs.length > 0 && (
                  <div className="context-section">
                    <h4>Recent Lab Trends</h4>
                    <ul>
                      {ragData.recent_labs.slice(0, 3).map((lab, idx) => (
                        <li key={idx}>
                          {lab.test_name}: {lab.value} {lab.unit}
                          {lab.trend && <span className="trend-indicator">{lab.trend}</span>}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                <p className="rag-source">🤖 Retrieved at {new Date(ragData.retrieved_at).toLocaleTimeString()}</p>
              </div>
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

        {/* RAG Clinical Assistant Chatbot */}
        <RAGChatbot
          mrn={mrn}
          patientName={summary.patientName}
          patientData={summary}
        />
      </div>
    </div>
  )
}

export default QuickView
