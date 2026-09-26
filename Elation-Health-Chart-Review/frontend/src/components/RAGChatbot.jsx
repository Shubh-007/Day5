import { useState, useRef, useEffect } from 'react'
import '../styles/chatbot.css'

function RAGChatbot({ mrn, patientName, patientData }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: `Hi! I'm your RAG clinical assistant for ${patientName}. I can help you understand:

• Drug interactions and medication safety
• Clinical guidelines for active conditions
• Lab value interpretations
• Preventive care recommendations
• Recent changes in the chart

What would you like to know about this patient?`,
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)
  const [isExpanded, setIsExpanded] = useState(false)

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async (e) => {
    e.preventDefault()

    if (!inputValue.trim()) return

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      text: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/tools/chat/rag', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_mrn: mrn,
          query: inputValue,
          conversation_history: messages.map(m => ({
            type: m.type,
            content: m.text
          }))
        })
      })

      if (!response.ok) throw new Error('Failed to get response')

      const data = await response.json()

      const botMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: data.response,
        sources: data.sources,
        confidence: data.confidence,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (err) {
      setError(err.message)
      const errorMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: `⚠️ I encountered an error: ${err.message}. Please try a different question.`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const suggestedQuestions = [
    "What are the drug interactions for this patient's medications?",
    "Are there any abnormal lab values I should be concerned about?",
    "What preventive care is overdue for this patient?",
    "Are there any contraindications I should know about?"
  ]

  const handleSuggestedQuestion = (question) => {
    setInputValue(question)
    setTimeout(() => {
      document.querySelector('.chatbot-input')?.focus()
    }, 0)
  }

  return (
    <div className={`rag-chatbot ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="chatbot-header" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="header-content">
          <h3>🤖 RAG Clinical Assistant</h3>
          <span className="toggle-arrow">{isExpanded ? '▼' : '▲'}</span>
        </div>
      </div>

      {isExpanded && (
        <div className="chatbot-container">
          <div className="messages-container">
            {messages.map(msg => (
              <div key={msg.id} className={`message ${msg.type}`}>
                <div className="message-content">
                  <p className="message-text">{msg.text}</p>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="message-sources">
                      <p className="sources-label">📚 Sources:</p>
                      <ul>
                        {msg.sources.map((source, idx) => (
                          <li key={idx}>{source}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {msg.confidence && (
                    <p className="confidence-badge">
                      Confidence: {(msg.confidence * 100).toFixed(0)}%
                    </p>
                  )}
                </div>
                <span className="message-time">
                  {msg.timestamp.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>
            ))}
            {loading && (
              <div className="message bot">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {!loading && messages.length === 1 && (
            <div className="suggested-questions">
              <p className="suggestions-label">Try asking:</p>
              <div className="suggestions-grid">
                {suggestedQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    className="suggestion-btn"
                    onClick={() => handleSuggestedQuestion(q)}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          <form className="chatbot-input-form" onSubmit={handleSendMessage}>
            <input
              type="text"
              className="chatbot-input"
              placeholder="Ask about medications, labs, guidelines..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={loading}
            />
            <button
              type="submit"
              className="send-btn"
              disabled={loading || !inputValue.trim()}
            >
              {loading ? '⏳' : '📤'}
            </button>
          </form>

          {error && (
            <div className="chatbot-error">
              {error}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RAGChatbot
