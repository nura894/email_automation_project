import { useState } from "react";
//import axios from "axios";
import api from "../../api/axios.js";

import { Link, useNavigate } from "react-router-dom";
import "./register.css";

function Register() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    smtp_password: ""
  });



  const [error, setError] = useState({});

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.name.trim()) {
      return setError({ name: "Name is required" });
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(form.email)) {
      return setError({ email: "Invalid email" });
    }

    if (form.password.length < 4) {
      return setError({ password: "Password must be at least 4 characters" });
    }

    if (!form.smtp_password.trim()) {
      return setError({ smtp_password: "SMTP password required" });
    }


    try {

      setError({});

      await api.post("/auth/signup", form);

      alert("User created");
      const res = await api.post(
        "/auth/login",
        new URLSearchParams({
          username: form.email,
          password: form.password
        })
      );

      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);

      navigate("/upload");

    } catch (err) {
      setError({
        general: err.response?.data?.detail || "Something went wrong"
      })
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2>Register</h2>

        <form onSubmit={handleSubmit}>
          <input
            placeholder="Name"
            onChange={(e) =>
              setForm({ ...form, name: e.target.value })
            }
          />
          {error && <p className="error-message">{error.name}</p>}

          <input
            placeholder="Email"
            onChange={(e) =>
              setForm({ ...form, email: e.target.value })
            }
          />
          {error && <p className="error-message">{error.email}</p>}

          <input
            type="password"
            placeholder="Password"
            autoComplete="new-password"
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
          />
          {error && <p className="error-message">{error.password}</p>}

          <input
            type="password"
            placeholder="SMTP Password"
            onChange={(e) =>
              setForm({ ...form, smtp_password: e.target.value })
            }
          />
          {error && <p className="error-message">{error.smtp_password}</p>}

          <button type="submit">Register</button>
          {error.general && (<p className="error-register">{error.general}</p>)}
        </form>

        <Link to="/" className="register-link">
          Login
        </Link>
      </div>
    </div>
  );
}

export default Register;