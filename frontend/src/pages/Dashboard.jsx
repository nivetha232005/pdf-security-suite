import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import UploadArea from '../components/UploadArea';
import ProgressBar from '../components/ProgressBar';
import Notification from '../components/Notification';
import * as api from '../services/api';

function Dashboard() {
  const [searchParams] = useSearchParams();
  const tool = searchParams.get('tool') || 'protect';
  
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [notification, setNotification] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [password, setPassword] = useState('');
  const [pageRange, setPageRange] = useState('');
  const [rotation, setRotation] = useState(90);
  const [downloadUrl, setDownloadUrl] = useState(null);

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  const handleUpload = async (files) => {
    setLoading(true);
    setProgress(0);
    
    const uploaded = [];
    let completed = 0;
    
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      
      // Validate file type
      if (!file.name.toLowerCase().endsWith('.pdf')) {
        showNotification(`${file.name} is not a PDF file`, 'error');
        completed++;
        setProgress((completed / files.length) * 100);
        continue;
      }
      
      // Validate file size (50MB max)
      if (file.size > 50 * 1024 * 1024) {
        showNotification(`${file.name} exceeds 50MB limit`, 'error');
        completed++;
        setProgress((completed / files.length) * 100);
        continue;
      }
      
      const result = await api.uploadPDF(file);
      if (result.success) {
        uploaded.push({ 
          file_id: result.file_id, 
          filename: result.filename,
          size: result.size || file.size 
        });
        showNotification(`${file.name} uploaded successfully`, 'success');
      } else {
        showNotification(`${file.name}: ${result.error || 'Upload failed'}`, 'error');
      }
      
      completed++;
      setProgress((completed / files.length) * 100);
    }
    
    setUploadedFiles(prev => [...prev, ...uploaded]);
    setLoading(false);
    setProgress(0);
    
    if (uploaded.length > 0) {
      showNotification(`${uploaded.length} file(s) uploaded successfully`, 'success');
    }
  };

  const removeFile = (index) => {
    const newFiles = [...uploadedFiles];
    newFiles.splice(index, 1);
    setUploadedFiles(newFiles);
    showNotification('File removed', 'info');
  };

  const moveFile = (index, direction) => {
    const newFiles = [...uploadedFiles];
    if (direction === 'up' && index > 0) {
      [newFiles[index], newFiles[index - 1]] = [newFiles[index - 1], newFiles[index]];
    } else if (direction === 'down' && index < newFiles.length - 1) {
      [newFiles[index], newFiles[index + 1]] = [newFiles[index + 1], newFiles[index]];
    }
    setUploadedFiles(newFiles);
  };

  const handleProtect = async () => {
    if (uploadedFiles.length === 0) {
      showNotification('Please upload a PDF first', 'error');
      return;
    }
    
    if (!password) {
      showNotification('Please enter a password', 'error');
      return;
    }
    
    setLoading(true);
    const result = await api.protectPDF(uploadedFiles[0].file_id, password);
    
    if (result.success) {
      setDownloadUrl(`http://localhost:5000${result.download_url}`);
      showNotification(result.message, 'success');
    } else {
      showNotification(result.error, 'error');
    }
    setLoading(false);
  };

  const handleRemovePassword = async () => {
    if (uploadedFiles.length === 0) {
      showNotification('Please upload a PDF first', 'error');
      return;
    }
    
    if (!password) {
      showNotification('Please enter the PDF password', 'error');
      return;
    }
    
    setLoading(true);
    const result = await api.removePassword(uploadedFiles[0].file_id, password);
    
    if (result.success) {
      setDownloadUrl(`http://localhost:5000${result.download_url}`);
      showNotification(result.message, 'success');
    } else {
      showNotification(result.error, 'error');
    }
    setLoading(false);
  };

  const handleMerge = async () => {
    if (uploadedFiles.length < 2) {
      showNotification('Please upload at least 2 PDFs to merge', 'error');
      return;
    }
    
    setLoading(true);
    const fileIds = uploadedFiles.map(f => f.file_id);
    const result = await api.mergePDFs(fileIds);
    
    if (result.success) {
      setDownloadUrl(`http://localhost:5000${result.download_url}`);
      showNotification(result.message, 'success');
    } else {
      showNotification(result.error, 'error');
    }
    setLoading(false);
  };

  const handleSplit = async () => {
    if (uploadedFiles.length === 0) {
      showNotification('Please upload a PDF first', 'error');
      return;
    }
    
    if (!pageRange) {
      showNotification('Please enter page range (e.g., 1-5 or 1,3,5)', 'error');
      return;
    }
    
    setLoading(true);
    const result = await api.splitPDF(uploadedFiles[0].file_id, pageRange);
    
    if (result.success) {
      setDownloadUrl(`http://localhost:5000${result.download_url}`);
      showNotification(result.message, 'success');
    } else {
      showNotification(result.error, 'error');
    }
    setLoading(false);
  };

  const handleCompress = async () => {
    if (uploadedFiles.length === 0) {
      showNotification('Please upload a PDF first', 'error');
      return;
    }
    
    setLoading(true);
    const result = await api.compressPDF(uploadedFiles[0].file_id);
    
    if (result.success) {
      setDownloadUrl(`http://localhost:5000${result.download_url}`);
      showNotification(`${result.message}. Reduction: ${result.reduction}%`, 'success');
    } else {
      showNotification(result.error, 'error');
    }
    setLoading(false);
  };

  const handleRotate = async () => {
    if (uploadedFiles.length === 0) {
      showNotification('Please upload a PDF first', 'error');
      return;
    }
    
    setLoading(true);
    const result = await api.rotatePDF(uploadedFiles[0].file_id, rotation);
    
    if (result.success) {
      setDownloadUrl(`http://localhost:5000${result.download_url}`);
      showNotification(result.message, 'success');
    } else {
      showNotification(result.error, 'error');
    }
    setLoading(false);
  };

  const renderToolInterface = () => {
    switch (tool) {
      case 'protect':
        return (
          <div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button className="btn btn-primary" onClick={handleProtect} disabled={loading}>
              Protect PDF
            </button>
          </div>
        );
      
      case 'remove':
        return (
          <div>
            <div className="form-group">
              <label>Current Password</label>
              <input
                type="password"
                placeholder="Enter PDF password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button className="btn btn-primary" onClick={handleRemovePassword} disabled={loading}>
              Remove Password
            </button>
          </div>
        );
      
      case 'merge':
        return (
          <div>
            <p style={{ marginBottom: '1rem' }}>
              <strong>Tip:</strong> You can reorder files using the ↑↓ buttons. The files will be merged in the order shown.
            </p>
            <button className="btn btn-primary" onClick={handleMerge} disabled={loading || uploadedFiles.length < 2}>
              Merge {uploadedFiles.length} PDFs
            </button>
          </div>
        );
      
      case 'split':
        return (
          <div>
            <div className="form-group">
              <label>Page Range</label>
              <input
                type="text"
                placeholder="e.g., 1-5 or 1,3,5"
                value={pageRange}
                onChange={(e) => setPageRange(e.target.value)}
              />
              <small>Examples: "1-5" (pages 1 to 5) or "1,3,5" (pages 1, 3, and 5)</small>
            </div>
            <button className="btn btn-primary" onClick={handleSplit} disabled={loading}>
              Split PDF
            </button>
          </div>
        );
      
      case 'compress':
        return (
          <div>
            <button className="btn btn-primary" onClick={handleCompress} disabled={loading}>
              Compress PDF
            </button>
          </div>
        );
      
      case 'rotate':
        return (
          <div>
            <div className="form-group">
              <label>Rotation Angle</label>
              <select value={rotation} onChange={(e) => setRotation(parseInt(e.target.value))}>
                <option value="90">90° Clockwise</option>
                <option value="180">180°</option>
                <option value="270">270° Clockwise</option>
              </select>
            </div>
            <button className="btn btn-primary" onClick={handleRotate} disabled={loading}>
              Rotate PDF
            </button>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="container" style={{ padding: '40px 20px' }}>
      <h1 style={{ marginBottom: '2rem' }}>PDF Tools Dashboard</h1>
      
      {downloadUrl && (
        <div className="download-card" style={{ marginBottom: '2rem' }}>
          <span>✅ Processed file ready!</span>
          <a href={downloadUrl} download className="btn btn-primary">
            Download
          </a>
        </div>
      )}
      
      <UploadArea 
        onUpload={handleUpload} 
        multiple={tool === 'merge'}
      />
      
      {uploadedFiles.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Uploaded Files {tool === 'merge' && '(Reorder for merge order)'}:</h3>
          {uploadedFiles.map((file, index) => (
            <div key={index} className="download-card" style={{ flexDirection: 'column', alignItems: 'stretch' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span><strong>{index + 1}.</strong> {file.filename}</span>
                <div>
                  {tool === 'merge' && (
                    <>
                      <button 
                        onClick={() => moveFile(index, 'up')} 
                        className="btn btn-secondary" 
                        style={{ marginRight: '0.5rem', padding: '0.25rem 0.5rem' }}
                        disabled={index === 0}
                      >
                        ↑
                      </button>
                      <button 
                        onClick={() => moveFile(index, 'down')} 
                        className="btn btn-secondary" 
                        style={{ marginRight: '0.5rem', padding: '0.25rem 0.5rem' }}
                        disabled={index === uploadedFiles.length - 1}
                      >
                        ↓
                      </button>
                    </>
                  )}
                  <button 
                    onClick={() => removeFile(index)} 
                    className="btn btn-danger" 
                    style={{ padding: '0.25rem 0.5rem' }}
                  >
                    Remove
                  </button>
                </div>
              </div>
              <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                Size: {(file.size / 1024).toFixed(2)} KB | ID: {file.file_id.substring(0, 8)}...
              </div>
            </div>
          ))}
        </div>
      )}
      
      {loading && <ProgressBar progress={progress} />}
      
      <div style={{ marginTop: '2rem' }}>
        {renderToolInterface()}
      </div>
      
      {notification && (
        <Notification
          message={notification.message}
          type={notification.type}
          onClose={() => setNotification(null)}
        />
      )}
    </div>
  );
}

export default Dashboard;