import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
const TOKEN_KEY = 'auth_token';
const USER_KEY = 'auth_user';

export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const getUser = () => {
  const user = localStorage.getItem(USER_KEY);
  return user ? JSON.parse(user) : null;
};

export const setAuthData = (token, user) => {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

export const clearAuthData = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearAuthData();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  signup: async (email, password, name) => {
    const response = await api.post('/api/auth/signup', { email, password, name });
    const { access_token, user } = response.data;
    setAuthData(access_token, user);
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post('/api/auth/login', { email, password });
    const { access_token, user } = response.data;
    setAuthData(access_token, user);
    return response.data;
  },

  logout: () => {
    clearAuthData();
  },

  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },

  isAuthenticated: () => {
    return !!getToken();
  },
};

export const chatAPI = {
  // Create a new chat
  createChat: async () => {
    const response = await api.post('/api/chats');
    return response.data;
  },

  // Get all chats
  getAllChats: async () => {
    const response = await api.get('/api/chats');
    return response.data;
  },

  // Get a specific chat
  getChat: async (chatId) => {
    const response = await api.get(`/api/chats/${chatId}`);
    return response.data;
  },

  // Delete a chat
  deleteChat: async (chatId) => {
    const response = await api.delete(`/api/chats/${chatId}`);
    return response.data;
  },

  // Send a message
  sendMessage: async (chatId, content) => {
    const response = await api.post(`/api/chats/${chatId}/messages`, {
      content,
    });
    return response.data;
  },
};

export default api;
