import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import Login from './components/Login';
import Signup from './components/Signup';
import { chatAPI, authAPI, getUser } from './services/api';
import './styles/App.css';

// Protected Route Component
const ProtectedRoute = ({ children, user }) => {
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

// Main Chat Component
const ChatApp = ({ user, onLogout }) => {
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Load all chats on mount
  useEffect(() => {
    loadChats();
  }, []);

  const loadChats = async () => {
    try {
      const chatList = await chatAPI.getAllChats();
      setChats(chatList);
    } catch (error) {
      console.error('Error loading chats:', error);
    }
  };

  const handleNewChat = async () => {
    try {
      const newChat = await chatAPI.createChat();
      setChats([newChat, ...chats]);
      setActiveChat(newChat);
      setMessages([]);
    } catch (error) {
      console.error('Error creating new chat:', error);
      alert('Failed to create new chat');
    }
  };

  const handleChatSelect = async (chatId) => {
    try {
      const chat = await chatAPI.getChat(chatId);
      setActiveChat(chat);
      setMessages(chat.messages || []);
    } catch (error) {
      console.error('Error loading chat:', error);
      alert('Failed to load chat');
    }
  };

  const handleDeleteChat = async (chatId) => {
    if (!window.confirm('Are you sure you want to delete this chat?')) {
      return;
    }

    try {
      await chatAPI.deleteChat(chatId);
      setChats(chats.filter(chat => chat.id !== chatId));
      
      // If the deleted chat was active, clear the chat area
      if (activeChat?.id === chatId) {
        setActiveChat(null);
        setMessages([]);
      }
    } catch (error) {
      console.error('Error deleting chat:', error);
      alert('Failed to delete chat');
    }
  };

  const handleSendMessage = async (content) => {
    let chatToUse = activeChat;
    
    // Create a new chat if none is active
    if (!chatToUse) {
      try {
        const newChat = await chatAPI.createChat();
        setChats([newChat, ...chats]);
        setActiveChat(newChat);
        setMessages([]);
        chatToUse = newChat;
      } catch (error) {
        console.error('Error creating new chat:', error);
        alert('Failed to create new chat');
        return;
      }
    }

    // Add user message to UI immediately
    const userMessage = {
      role: 'user',
      content: content,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage(chatToUse.id, content);
      
      // Add assistant response
      setMessages(prev => [...prev, response]);
      
      // Reload chats to update the sidebar (title may have changed)
      loadChats();
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message. Please try again.');
      // Remove the user message if the request failed
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <Sidebar
        chats={chats}
        activeChat={activeChat}
        onChatSelect={handleChatSelect}
        onNewChat={handleNewChat}
        onDeleteChat={handleDeleteChat}
        user={user}
        onLogout={onLogout}
      />
      <ChatArea
        activeChat={activeChat}
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
};

function App() {
  const [user, setUser] = useState(getUser());

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleSignup = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    authAPI.logout();
    setUser(null);
  };

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={
            user ? <Navigate to="/" replace /> : <Login onLogin={handleLogin} />
          } 
        />
        <Route 
          path="/signup" 
          element={
            user ? <Navigate to="/" replace /> : <Signup onSignup={handleSignup} />
          } 
        />
        <Route
          path="/"
          element={
            <ProtectedRoute user={user}>
              <ChatApp user={user} onLogout={handleLogout} />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
