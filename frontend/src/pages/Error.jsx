import React from 'react';
import { Link } from 'react-router-dom';

function Error() {
  return (
    <div className="container" style={{ textAlign: 'center', padding: '100px 20px' }}>
      <h1 style={{ fontSize: '4rem', color: 'var(--danger-color)' }}>404</h1>
      <h2 style={{ marginTop: '1rem' }}>Page Not Found</h2>
      <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Link to="/" className="btn btn-primary" style={{ marginTop: '2rem', display: 'inline-block' }}>
        Go Home
      </Link>
    </div>
  );
}

export default Error;