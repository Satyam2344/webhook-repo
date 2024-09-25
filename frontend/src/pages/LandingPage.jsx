import React, { } from "react";

import { Link } from 'react-router-dom';
import '../css/LandingPage.css';

export default function LandingPage() {

    return (
        <>
            <h1>Check The Actions Summary</h1>
            <p>Get the new way to look the GitHub</p>
            <div class="frame">
                <Link to="/register"><button class="custom-btn btn-5"><span>Sign Up</span></button></Link>
                <Link to="/login"><button class="custom-btn btn-6"><span>Login</span></button></Link>
            </div>
        </>
    );
}