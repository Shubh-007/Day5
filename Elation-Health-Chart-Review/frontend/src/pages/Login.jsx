import React, { useState } from 'react';
import { apiFetch, setToken } from '../api/client';
import '../styles/login.css';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const response = await apiFetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      // Store token and user info
      setToken(data.access_token, data.role, data.display_name);

      // Notify parent component
      if (onLogin) {
        onLogin({
          username,
          role: data.role,
          displayName: data.display_name,
        });
      }
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Elation Health Chart Review</h1>
        <p className="subtitle">Secure Clinical Documentation Assistant</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              disabled={loading}
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={loading} className="login-button">
            {loading ? 'Logging in...' : 'Log In'}
          </button>
        </form>

        <div className="demo-credentials">
          <h3>Demo Credentials</h3>
          <div className="cred">
            <strong>Admin:</strong> admin / demo-admin-2026
          </div>
          <div className="cred">
            <strong>Dr. Chen:</strong> schen / demo-schen-2026
          </div>
          <div className="cred">
            <strong>Dr. Park:</strong> mpark / demo-mpark-2026
          </div>
        </div>
      </div>
    </div>
  );
}
