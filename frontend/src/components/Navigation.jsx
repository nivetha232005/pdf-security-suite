import React from 'react';
import { Link } from 'react-router-dom';

function Navigation({ darkMode, toggleDarkMode }) {
  return (
    <nav className="navbar">
      <div className="container nav-container">
        <Link to="/" className="logo">PDF Security Suite</Link>
        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/about">About</Link>
          <Link to="/contact">Contact</Link>
          <button onClick={toggleDarkMode} className="dark-mode-toggle">
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;