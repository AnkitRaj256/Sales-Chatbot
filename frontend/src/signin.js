import React, { useState } from "react";
import "./signin.css";

const Signin = ({ setPage }) => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (response.ok) {
        setMessage("User registered successfully! Redirecting to login...");
        setTimeout(() => setPage("login"), 2000);
      } else {
        setMessage(result.error || "Error registering user.");
      }
    } catch (error) {
      setMessage("Error connecting to server.");
    }
  };

  return (
    <div className="signin-page">
      <div className="form-container animated-form">
        <form onSubmit={handleSubmit} className="signin-form">
          <h2>Sign Up</h2>

          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              placeholder="Enter your username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="btn-submit">
            Register
          </button>

          {message && <p className="message">{message}</p>}

          <p className="login-link">
            Already a user?{" "}
            <span onClick={() => setPage("login")} className="login-text">
              Login
            </span>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Signin;
