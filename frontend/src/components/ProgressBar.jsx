import React from 'react';

function ProgressBar({ progress }) {
  return (
    <div className="progress-container">
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
      </div>
      <p style={{ textAlign: 'center', marginTop: '0.5rem' }}>{progress}%</p>
    </div>
  );
}

export default ProgressBar;