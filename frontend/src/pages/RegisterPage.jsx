import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import '../css/RegisterPage.css';
import config from '../config.json';

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [github_url, setGithub_url] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errors, setErrors] = useState({});
    const navigate = useNavigate();
    const GitHub_URL = config.GUTHUB_URL_REGISTER;

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (password !== confirmPassword) {
            setErrors({ password: 'Passwords do not match' });
            return;
        }

        const data = { username, email, github_url, password };
        const response = await fetch(GitHub_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        if (result.error) {
            setErrors(result.error);
            alert(result.error);
            // Clear all fields
            setUsername('');
            setPassword('');
            setGithub_url('');
            setEmail('');
            setConfirmPassword('');
        } else {
            console.log('User created successfully');
            navigate("/login");
        }
    };

    return (
        <div className="signup-container">
            <h1>Signup</h1>
            <form onSubmit={handleSubmit}>
                <label>Username:</label>
                <input type="text" name='username' value={username} onChange={(event) => setUsername(event.target.value)} required min={3} max={12} />
                {errors.username && <div style={{ color: 'red' }}>{errors.username}</div>}
                <br />
                <label>Email:</label>
                <input type="email" name='email' value={email} onChange={(event) => setEmail(event.target.value)} required />
                {errors.email && <div style={{ color: 'red' }}>{errors.email}</div>}
                <br />
                <label>GitHub URL:</label>
                <input type="text" name='github_url' value={github_url} onChange={(event) => setGithub_url(event.target.value)} required />
                {errors.github_url && <div style={{ color: 'red' }}>{errors.github_url}</div>}
                <br />
                <label>Password:</label>
                <input type="password" name='password' value={password} onChange={(event) => setPassword(event.target.value)} required min={8} />
                {errors.password && <div style={{ color: 'red' }}>{errors.password}</div>}
                <br />
                <label>Confirm Password:</label>
                <input type="password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} required min={8} />
                {errors.confirmPassword && <div style={{ color: 'red' }}>{errors.confirmPassword}</div>}
                <br />
                <button type="submit">Signup</button>
            </form>
        </div>
    );
};

export default RegisterPage;