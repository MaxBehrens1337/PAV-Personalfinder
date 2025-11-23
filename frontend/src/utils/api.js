/**
 * API Client Configuration
 * Axios instance with interceptors for authentication
 */

import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API methods
export const authAPI = {
  login: (username, password) =>
    api.post('/api/auth/login', `username=${username}&password=${password}`, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  logout: () => api.post('/api/auth/logout'),
  getCurrentUser: () => api.get('/api/auth/me'),
};

export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard/stats'),
  getRecentActivity: (limit = 10) => api.get(`/api/dashboard/recent-activity?limit=${limit}`),
};

export const mitarbeiterAPI = {
  list: (params) => api.get('/api/mitarbeiter/', { params }),
  get: (id) => api.get(`/api/mitarbeiter/${id}`),
  create: (data) => api.post('/api/mitarbeiter/', data),
  update: (id, data) => api.patch(`/api/mitarbeiter/${id}`, data),
  delete: (id) => api.delete(`/api/mitarbeiter/${id}`),
};

export const aiMatchingAPI = {
  search: (data) => api.post('/api/ai-match/search', data),
  reindex: () => api.post('/api/ai-match/reindex'),
  getStatus: () => api.get('/api/ai-match/status'),
};

export const qualifikationAPI = {
  list: () => api.get('/api/qualifikationen/'),
  create: (data) => api.post('/api/qualifikationen/', data),
  addToMitarbeiter: (mitarbeiterId, data) =>
    api.post(`/api/qualifikationen/mitarbeiter/${mitarbeiterId}`, data),
};

export const verfuegbarkeitAPI = {
  getForMitarbeiter: (mitarbeiterId, fromDate, toDate) =>
    api.get(`/api/verfuegbarkeit/mitarbeiter/${mitarbeiterId}`, {
      params: { from_date: fromDate, to_date: toDate },
    }),
  create: (data) => api.post('/api/verfuegbarkeit/', data),
  delete: (id) => api.delete(`/api/verfuegbarkeit/${id}`),
};

export const userAPI = {
  list: () => api.get('/api/users/'),
  get: (id) => api.get(`/api/users/${id}`),
  create: (data) => api.post('/api/users/', data),
  update: (id, data) => api.patch(`/api/users/${id}`, data),
  delete: (id) => api.delete(`/api/users/${id}`),
};

export default api;
