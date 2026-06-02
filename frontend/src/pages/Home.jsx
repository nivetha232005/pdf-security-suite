import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  const tools = [
    { icon: '🔒', title: 'Password Protection', description: 'Secure your PDFs with strong encryption', path: '/dashboard?tool=protect' },
    { icon: '🔓', title: 'Remove Password', description: 'Unlock password-protected PDFs', path: '/dashboard?tool=remove' },
    { icon: '📚', title: 'Merge PDFs', description: 'Combine multiple PDFs into one', path: '/dashboard?tool=merge' },
    { icon: '✂️', title: 'Split PDF', description: 'Extract specific pages', path: '/dashboard?tool=split' },
    { icon: '📦', title: 'Compress PDF', description: 'Reduce file size', path: '/dashboard?tool=compress' },
    { icon: '🔄', title: 'Rotate PDF', description: 'Rotate pages as needed', path: '/dashboard?tool=rotate' }
  ];

  return (
    <div>
      <section className="hero">
        <div className="container">
          <h1>PDF Security Suite</h1>
          <p>Professional PDF management tools with enterprise-grade security</p>
          <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>
            Get Started
          </button>
        </div>
      </section>

      <div className="container">
        <div className="tools-grid">
          {tools.map((tool, index) => (
            <div key={index} className="tool-card" onClick={() => navigate(tool.path)}>
              <div className="tool-icon">{tool.icon}</div>
              <h3>{tool.title}</h3>
              <p>{tool.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Home;