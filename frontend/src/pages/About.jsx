import React from 'react';

function About() {
  return (
    <div className="container" style={{ padding: '60px 20px' }}>
      <h1>About PDF Security Suite</h1>
      <div style={{ marginTop: '2rem' }}>
        <p style={{ fontSize: '1.1rem', lineHeight: '1.6', marginBottom: '1rem' }}>
          PDF Security Suite is a professional, enterprise-grade PDF management platform 
          built with modern web technologies.
        </p>
        
        <h2 style={{ marginTop: '2rem', marginBottom: '1rem' }}>Key Features</h2>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ marginBottom: '0.5rem' }}>✓ Password protection with AES encryption</li>
          <li style={{ marginBottom: '0.5rem' }}>✓ Remove passwords from protected PDFs</li>
          <li style={{ marginBottom: '0.5rem' }}>✓ Merge multiple PDFs into one document</li>
          <li style={{ marginBottom: '0.5rem' }}>✓ Split PDFs by page ranges</li>
          <li style={{ marginBottom: '0.5rem' }}>✓ Compress PDFs to reduce file size</li>
          <li style={{ marginBottom: '0.5rem' }}>✓ Rotate PDF pages</li>
        </ul>
      </div>
    </div>
  );
}

export default About;
