import React, { useState } from 'react';

function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Thank you for your message! We will get back to you soon.');
    setFormData({ name: '', email: '', message: '' });
  };

  return (
    <div className="container" style={{ padding: '60px 20px' }}>
      <h1>Contact Us</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem', marginTop: '2rem' }}>
        <div>
          <h3>Get in Touch</h3>
          <p style={{ marginTop: '1rem', lineHeight: '1.6' }}>
            Have questions about PDF Security Suite? Need help with a specific feature?
            We're here to help! Fill out the form and we'll get back to you within 24 hours.
          </p>
          
          <div style={{ marginTop: '2rem' }}>
            <h4>Email</h4>
            <p>will be updated soon</p>
            
            <h4 style={{ marginTop: '1rem' }}>Hours</h4>
            <p>Monday - Friday: 9 AM - 6 PM EST</p>
          </div>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Message</label>
            <textarea
              rows="5"
              value={formData.message}
              onChange={(e) => setFormData({ ...formData, message: e.target.value })}
              required
            ></textarea>
          </div>
          
          <button type="submit" className="btn btn-primary">Send Message</button>
        </form>
      </div>
    </div>
  );
}

export default Contact;