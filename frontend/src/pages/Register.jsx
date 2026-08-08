import { useState } from "react";
import api from "../api/client";
import "../App.css";

function Register({ onLogin, onBackToLogin }) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await api.post("/users/register", {
        first_name: firstName,
        last_name: lastName,
        username,
        email,
        password,
      });

      setSuccess(
        "Account created successfully! Redirecting to login..."
      );

      setTimeout(() => {
        onBackToLogin();
      }, 1200);
    } catch (err) {
      console.log("REGISTER ERROR:", err.response?.data);

      const detail = err.response?.data?.detail;

      if (Array.isArray(detail)) {
        setError(
          detail.map((item) => item.msg).join(", ")
        );
      } else {
        setError(
          detail || "Registration failed. Please try again."
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
            <h1>Create your account</h1>
            <p>
              Start turning your documents into knowledge.
            </p>
          </div>

          <form
            onSubmit={handleRegister}
            className="auth-form"
          >

            <div className="form-row">

              <div className="form-group">
                <label htmlFor="firstName">
                  First name
                </label>

                <input
                  id="firstName"
                  type="text"
                  placeholder="First name"
                  value={firstName}
                  onChange={(e) =>
                    setFirstName(e.target.value)
                  }
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="lastName">
                  Last name
                </label>

                <input
                  id="lastName"
                  type="text"
                  placeholder="Last name"
                  value={lastName}
                  onChange={(e) =>
                    setLastName(e.target.value)
                  }
                  required
                />
              </div>

            </div>

            <div className="form-group">
              <label htmlFor="username">
                Username
              </label>

              <input
                id="username"
                type="text"
                placeholder="Choose a username"
                value={username}
                onChange={(e) =>
                  setUsername(e.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">
                Email
              </label>

              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) =>
                  setEmail(e.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="registerPassword">
                Password
              </label>

              <input
                id="registerPassword"
                type="password"
                placeholder="Create a password"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
                required
              />
            </div>

            {error && (
              <div className="auth-error">
                {error}
              </div>
            )}

            {success && (
              <div className="auth-success">
                {success}
              </div>
            )}

            <button
              type="submit"
              className="primary-button"
              disabled={loading}
            >
              {loading
                ? "Creating account..."
                : "Create account"}
            </button>

          </form>

          <div className="auth-divider">
            <span>or</span>
          </div>

          <p className="auth-switch">
            Already have an account?{" "}

            <button
              type="button"
              className="link-button"
              onClick={onBackToLogin}
            >
              Sign in
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

export default Register;