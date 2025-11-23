/**
 * Global State Management with Zustand
 */

import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('access_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),

  login: (token, user) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ token, user, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    set({ token: null, user: null, isAuthenticated: false });
  },

  updateUser: (user) => {
    localStorage.setItem('user', JSON.stringify(user));
    set({ user });
  },
}));

export const useDashboardStore = create((set) => ({
  stats: null,
  recentActivity: null,
  loading: false,
  error: null,

  setStats: (stats) => set({ stats }),
  setRecentActivity: (activity) => set({ recentActivity: activity }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));

export const useMitarbeiterStore = create((set) => ({
  mitarbeiter: [],
  currentMitarbeiter: null,
  total: 0,
  loading: false,
  error: null,

  setMitarbeiter: (mitarbeiter, total) => set({ mitarbeiter, total }),
  setCurrentMitarbeiter: (mitarbeiter) => set({ currentMitarbeiter: mitarbeiter }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  reset: () => set({ mitarbeiter: [], currentMitarbeiter: null, total: 0, loading: false, error: null }),
}));

export const useAIMatchingStore = create((set) => ({
  query: '',
  matches: [],
  totalMatches: 0,
  aiEnabled: false,
  loading: false,
  error: null,
  executionTime: 0,

  setQuery: (query) => set({ query }),
  setMatches: (matches, totalMatches, aiEnabled, executionTime) =>
    set({ matches, totalMatches, aiEnabled, executionTime }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  reset: () => set({ query: '', matches: [], totalMatches: 0, loading: false, error: null, executionTime: 0 }),
}));
