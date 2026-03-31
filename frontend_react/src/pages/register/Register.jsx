import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "./register.css";

function Register() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    smtp_password: ""
  });

  const [error, setError] = useState(""); 

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setError(""); 

      await axios.post("http://localhost:8000/auth/signup", form);

      alert("User created");
    } catch (err) {
      const msg = err.response?.data?.detail || "Something went wrong";

      setError(msg); 
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

          <input
            placeholder="Email"
            onChange={(e) =>
              setForm({ ...form, email: e.target.value })
            }
          />

          <input
            type="password"
            placeholder="Password"
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
          />

          <input
            type="password"
            placeholder="SMTP Password"
            onChange={(e) =>
              setForm({ ...form, smtp_password: e.target.value })
            }
          />
          {error && <p className="error-message">{error}</p>}
          <button type="submit">Register</button>
        </form>

        <Link to="/" className="register-link">
          Login
        </Link>
      </div>
    </div>
  );
}

export default Register;