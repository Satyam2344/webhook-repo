import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import '../css/LoginPage.css';
import config from '../config.json';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const GitHub_URL_LOGIN = config.GUTHUB_URL_LOGIN;
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        fetch(GitHub_URL_LOGIN, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    // Login successful, redirect to dashboard or whatever
                    navigate(`/dashboard/${email}`);
                } else {
                    setError(data.error);
                    // Clear all fields
                    setEmail('');
                    setPassword('');
                }
            })
            .catch((error) => {
                setError('An error occurred. Please try again.');
                // Clear all fields
                setEmail('');
                setPassword('');
            });
    };

    return (
        <div className="login-container">
            <form onSubmit={handleSubmit}>
                <h2>Login</h2>
                <label>Email:</label>
                <input type="email" value={email} name='email' onChange={(event) => setEmail(event.target.value)} />
                <br />
                <label>Password:</label>
                <input type="password" value={password} name='password' onChange={(event) => setPassword(event.target.value)} />
                <br />
                {error && (
                    <div style={{ color: 'red' }}>
                        {error}
                        <button onClick={() => setError(null)}>×</button>
                    </div>
                )}
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;