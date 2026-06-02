import React, { useEffect } from 'react';

function Notification({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 5000);

    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`notification ${type}`}>
      <strong>{type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ'}</strong>
      <span>{message}</span>
    </div>
  );
}

export default Notification;