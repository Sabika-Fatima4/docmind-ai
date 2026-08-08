import { useState } from "react";
import api from "../api/client";
import "../App.css";

function Login({ onLogin, onRegister }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await api.post("/users/login", {
        username,
        password,
      });

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      onLogin();
    } catch (err) {
      console.log("LOGIN ERROR:", err.response?.data);

      const detail = err.response?.data?.detail;

      if (Array.isArray(detail)) {
        setError(
          detail.map((item) => item.msg).join(", ")
        );
      } else {
        setError(
          detail ||
            "Login failed. Please check your credentials."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-glow"></div>

      <div className="auth-container">
        <div className="brand">
          <div className="brand-icon">✦</div>
          <span>DocMind AI</span>
        </div>

        <div className="auth-card">
          <div className="auth-header">
            <h1>Welcome back</h1>
            <p>
              Sign in to continue working with your documents.
            </p>
          </div>

          <form onSubmit={handleLogin} className="auth-form">
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                id="username"
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            {error && (
              <div className="auth-error">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="primary-button"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>

          <div className="auth-divider">
            <span>or</span>
          </div>

          <p className="auth-switch">
            Don't have an account?{" "}
            <button
              type="button"
              className="link-button"
              onClick={onRegister}
            >
              Create one
            </button>
          </p>
        </div>

        <p className="auth-footer">
          Your documents. Your knowledge. One intelligent workspace.
        </p>
      </div>
    </div>
  );
}

export default Login;