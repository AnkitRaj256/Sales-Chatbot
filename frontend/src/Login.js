import React, { useState } from "react";
import './Login.css';

const Login = ({ setPage, setIsAuthenticated }) => {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });
    const [error, setError] = useState("");

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            const result = await response.json();
            if (response.ok) {
                setIsAuthenticated(true);
                setPage("chatbot"); // Go to Chatbot
            } else {
                setError(result.error || "Invalid credentials.");
            }
        } catch (err) {
            setError("Error connecting to server.");
        }
    };

    return (
        <div className="login-container">
            <form onSubmit={handleSubmit} className="login-form">
                <h2>Login</h2>

                <div className="input-group">
                    <label>Username</label>
                    <input
                        type="text"
                        name="username"
                        placeholder="Enter your username"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="input-group">
                    <label>Password</label>
                    <input
                        type="password"
                        name="password"
                        placeholder="Enter your password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>

                <button type="submit" className="login-btn">Login</button>
                {error && <p className="error-message">{error}</p>}

                <div className="login-footer">
                    <p>New user? <span onClick={() => setPage("signin")} className="login-text">
                      SignUp
                    </span></p>
                </div>
            </form>
        </div>
    );
};

export default Login;
