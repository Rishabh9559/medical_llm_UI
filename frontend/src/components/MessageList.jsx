import React, { useRef, useEffect } from 'react';
import '../styles/MessageList.css';

const MessageList = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="message-list">
      {messages.length === 0 && !isLoading && (
        <div className="welcome-message">
          <h2>Medical Assistant</h2>
          <p>Hello! I'm your medical assistant. How can I help you today?</p>
        </div>
      )}
      {messages.map((message, index) => (
        <div
          key={index}
          className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
        >
          <div className="message-avatar">
            {message.role === 'user' ? '👤' : '🏥'}
          </div>
          <div className="message-content">
            <div className="message-text">{message.content}</div>
          </div>
        </div>
      ))}
      {isLoading && (
        <div className="message assistant-message">
          <div className="message-avatar">🏥</div>
          <div className="message-content">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
