import { useState } from "react";
import api from "../../api/axios.js";
import { Link, useNavigate } from "react-router-dom";
import './login.css'

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();
  const [error, setError] = useState({});

  const handleLogin = async (e) => {
    e.preventDefault();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      return setError({ email: "Invalid email" });
    }

    if (password.length < 4) {
      return setError({ password: "Password must be at least 4 characters" });
    }

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
      const res = await api.post(
        "/auth/login",
        formData
      );

      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);

      console.log("Login success");

      navigate("/upload");

    } catch (err) {
      const message =
        err.response?.data?.detail || "Login failed";
      setError({ general: message });
    }
  };


  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Login</h2>

        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />
          {error.email && <p className="error-message">{error.email}</p>}

          <input
            type="password"
            placeholder="Password"
           // autoComplete="new-password"
            onChange={(e) => setPassword(e.target.value)}
          />
          {error.password && <p className="error-message">{error.password}</p>}

          <button type="submit">Submit</button>
          {error.general && <p className="error-login">{error.general}</p>}
        </form>

        <Link to="/register" className="login-link">
          Register
        </Link>

      </div>
    </div>
  );
}

export default Login;