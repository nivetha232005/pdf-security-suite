import React, { useRef, useState } from 'react';

function UploadArea({ onUpload, multiple = false, accept = ".pdf" }) {
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      onUpload(files);
    }
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      onUpload(files);
    }
  };

  return (
    <div
      className={`upload-area ${dragOver ? 'drag-over' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => fileInputRef.current.click()}
    >
      <div className="upload-icon">📄</div>
      <h3>Drop your PDF{multiple ? 's' : ''} here or click to browse</h3>
      <p>Maximum file size: 50MB per file</p>
      <p>{multiple ? 'You can select multiple PDF files' : 'Select one PDF file'}</p>
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        multiple={multiple}
        onChange={handleFileSelect}
      />
    </div>
  );
}

export default UploadArea;