import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const fetchMachines = async (filters = {}) => {
  try {
    const params = new URLSearchParams();
    if (filters.os) params.append('os', filters.os);
    if (filters.status) params.append('status', filters.status);
    if (filters.limit) params.append('limit', filters.limit);
    if (filters.offset) params.append('offset', filters.offset);
    
    const response = await api.get(`/machines?${params.toString()}`);
    return response;
  } catch (error) {
    throw new Error('Failed to fetch machines');
  }
};

export const fetchMachineById = async (id) => {
  try {
    const response = await api.get(`/machines/${id}`);
    return response;
  } catch (error) {
    throw new Error('Failed to fetch machine details');
  }
};

export const reportMachineStatus = async (payload) => {
  try {
    const response = await api.post('/report', payload);
    return response;
  } catch (error) {
    throw new Error('Failed to report machine status');
  }
};

export const exportData = async (format = 'csv') => {
  try {
    const response = await api.get(`/export?format=${format}`, {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `system-utility-report.${format}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    
    return response;
  } catch (error) {
    throw new Error('Failed to export data');
  }
};

export default api; 