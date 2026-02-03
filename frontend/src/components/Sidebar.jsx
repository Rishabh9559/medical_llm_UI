import React from 'react';
import ChatItem from './ChatItem';
import '../styles/Sidebar.css';

const Sidebar = ({ chats, activeChat, onChatSelect, onNewChat, onDeleteChat }) => {
  return (
    <div className="sidebar">
      <button className="new-chat-btn" onClick={onNewChat}>
        + New Chat
      </button>
      <div className="chat-list">
        {chats.length === 0 ? (
          <div className="no-chats">No chats yet. Start a new conversation!</div>
        ) : (
          chats.map((chat) => (
            <ChatItem
              key={chat.id}
              chat={chat}
              isActive={activeChat?.id === chat.id}
              onClick={() => onChatSelect(chat.id)}
              onDelete={onDeleteChat}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default Sidebar;
