import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.error || 'Upload failed' };
  }
};

export const protectPDF = async (fileId, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/protect`, { file_id: fileId, password });
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.error || 'Protection failed' };
  }
};

export const removePassword = async (fileId, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/remove-password`, { file_id: fileId, password });
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.error || 'Failed to remove password' };
  }
};

export const mergePDFs = async (fileIds) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/merge`, { file_ids: fileIds });
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.error || 'Merge failed' };
  }
};

export const splitPDF = async (fileId, pageRange) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/split`, { file_id: fileId, page_range: pageRange });
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.error || 'Split failed' };
  }
};

export const compressPDF = async (fileId) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/compress`, { file_id: fileId });
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.error || 'Compression failed' };
  }
};

export const rotatePDF = async (fileId, rotation) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/rotate`, { file_id: fileId, rotation });
    return response.data;
  } catch (error) {
    return { error: error.response?.data?.error || 'Rotation failed' };
  }
};

// Add this function to handle downloads
export const downloadFile = (downloadUrl) => {
  const fullUrl = downloadUrl.startsWith('http') 
    ? downloadUrl 
    : 'https://pdf-security-suite-backend.onrender.com' + downloadUrl;
  
  window.open(fullUrl, '_blank');
};
