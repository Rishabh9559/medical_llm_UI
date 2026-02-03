import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
