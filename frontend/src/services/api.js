import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    console.log(`API Request to ${config.url}:`, {
      hasToken: !!token,
      tokenStart: token ? token.substring(0, 20) + '...' : 'none'
    });
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      console.error('401 Error:', error.response);
      console.log('Request headers:', error.config?.headers);
      console.log('Token in localStorage:', localStorage.getItem('token') ? 'exists' : 'missing');

      // Don't redirect immediately - let's debug first
      // const currentPath = window.location.pathname;
      // if (currentPath !== '/login' && currentPath !== '/signup') {
      //   localStorage.removeItem('token');
      //   localStorage.removeItem('user');
      //   window.location.href = '/login';
      // }
    }
    return Promise.reject(error);
  }
);

export default api;