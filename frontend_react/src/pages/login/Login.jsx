import { useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import './login.css'

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
      const res = await axios.post(
        "http://localhost:8000/auth/login",
        formData
      );

      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);

      console.log("Login success");

      navigate("/upload");

    } catch (err) {
      console.error("Login failed", err);
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

          <input
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">Submit</button>
        </form>

        <Link to="/register" className="login-link">
          Register
        </Link>
        
      </div>
    </div>
  );
}

export default Login;