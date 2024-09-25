import React, { } from 'react';
import './App.css';

import { BrowserRouter, Routes, Route } from 'react-router-dom';


import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage';
import LandingPage from './pages/LandingPage';
import './App.css';

function App() {
  return (
    <div className="vh-100 gradient-custom">
      <div className="container">
        <h1 className="page-header text-center">GitHub Actions Details</h1>

        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/dashboard/:email" element={<DashboardPage />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;