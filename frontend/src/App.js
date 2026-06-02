import axios from 'axios';

// Use environment variable for API URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://pdf-security-suite-1.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Rest of your API functions remain the same...
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
    console.error('Upload error:', error);
    return { error: error.response?.data?.error || 'Upload failed' };
  }
};

export const protectPDF = async (fileId, password) => {
  try {
    const response = await api.post('/protect', { file_id: fileId, password });
    return response.data;
  } catch (error) {
    console.error('Protect error:', error);
    return { error: error.response?.data?.error || 'Protection failed' };
  }
};

export const removePassword = async (fileId, password) => {
  try {
    const response = await api.post('/remove-password', { file_id: fileId, password });
    return response.data;
  } catch (error) {
    console.error('Remove password error:', error);
    return { error: error.response?.data?.error || 'Failed to remove password' };
  }
};

export const mergePDFs = async (fileIds) => {
  try {
    const response = await api.post('/merge', { file_ids: fileIds });
    return response.data;
  } catch (error) {
    console.error('Merge error:', error);
    return { error: error.response?.data?.error || 'Merge failed' };
  }
};

export const splitPDF = async (fileId, pageRange) => {
  try {
    const response = await api.post('/split', { file_id: fileId, page_range: pageRange });
    return response.data;
  } catch (error) {
    console.error('Split error:', error);
    return { error: error.response?.data?.error || 'Split failed' };
  }
};

export const compressPDF = async (fileId) => {
  try {
    const response = await api.post('/compress', { file_id: fileId });
    return response.data;
  } catch (error) {
    console.error('Compress error:', error);
    return { error: error.response?.data?.error || 'Compression failed' };
  }
};

export const rotatePDF = async (fileId, rotation) => {
  try {
    const response = await api.post('/rotate', { file_id: fileId, rotation });
    return response.data;
  } catch (error) {
    console.error('Rotate error:', error);
    return { error: error.response?.data?.error || 'Rotation failed' };
  }
};
