/**
 * Shared authenticated API client
 * Handles JWT token injection, 401/403 responses, and auth state
 */

let onUnauthorized = null;

export function setUnauthorizedCallback(callback) {
  onUnauthorized = callback;
}

export function getToken() {
  return sessionStorage.getItem("access_token");
}

export function setToken(token, role, displayName) {
  sessionStorage.setItem("access_token", token);
  sessionStorage.setItem("role", role);
  sessionStorage.setItem("display_name", displayName);
}

export function clearToken() {
  sessionStorage.removeItem("access_token");
  sessionStorage.removeItem("role");
  sessionStorage.removeItem("display_name");
}

export function getAuthState() {
  const token = getToken();
  const role = sessionStorage.getItem("role");
  const displayName = sessionStorage.getItem("display_name");

  if (token && role && displayName) {
    return { token, role, displayName };
  }
  return null;
}

/**
 * Authenticated fetch wrapper
 * Automatically injects Authorization header and handles 401/403
 */
export async function apiFetch(path, options = {}) {
  const token = getToken();

  // Prepare headers
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Inject auth token if available
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(path, {
      ...options,
      headers,
    });

    // Handle 401 Unauthorized
    if (response.status === 401) {
      clearToken();
      if (onUnauthorized) {
        onUnauthorized();
      }
      throw new Error("Unauthorized: Session expired. Please log in again.");
    }

    // Handle 403 Forbidden
    if (response.status === 403) {
      const error = new Error("Access denied: You don't have permission to access this resource.");
      error.isForbidden = true;
      throw error;
    }

    // Other errors
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: response.statusText }));
      const message = error.detail || error.message || response.statusText;
      throw new Error(`API Error (${response.status}): ${message}`);
    }

    return response;
  } catch (error) {
    console.error("API fetch error:", error);
    throw error;
  }
}
