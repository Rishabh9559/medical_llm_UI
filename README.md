# Medical LLM Chatbot UI

A full-stack ChatGPT-like chatbot interface for a medical LLM assistant with chat history management and MongoDB storage.

## Features

- **ChatGPT-like UI Interface**: Clean, modern chat interface with responsive design
- **Chat History Management**: Sidebar showing previous conversations with timestamps
- **Context-Aware Conversations**: Maintains context by sending last 4 messages to the LLM
- **MongoDB Integration**: Persistent storage for all chats and messages
- **Real-time Responses**: Typing indicators and auto-scroll to latest messages
- **Chat Management**: Create, view, and delete chat conversations

## Tech Stack

- **Frontend**: React.js with Vite
- **Backend**: Python FastAPI
- **Database**: MongoDB
- **LLM API**: Custom medical LLM endpoint

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (v4.4 or higher)
- **npm** or **yarn** package manager

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Rishabh9559/medical_llm_UI.git
cd medical_llm_UI
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
MONGODB_URL=mongodb://localhost:27017  # Or use MongoDB Atlas connection string
DATABASE_NAME=medical_llm_db
LLM_API_URL=your-llm-api-url-here
LLM_API_KEY=your-api-key-here
LLM_MODEL=your-model-name-here
```

**Note:** You can use either a local MongoDB instance or MongoDB Atlas. For MongoDB Atlas, use a connection string like:
```
mongodb+srv://username:password@cluster.mongodb.net/?appName=YourApp
```

#### Start MongoDB (if using local MongoDB)

If using a local MongoDB instance, make sure it's running:

```bash
# For macOS with Homebrew
brew services start mongodb-community

# For Linux with systemd
sudo systemctl start mongod

# Or run MongoDB directly
mongod --dbpath /path/to/your/data/directory
```

#### Run the Backend

```bash
python main.py
```

The backend server will start at `http://localhost:8000`

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd ../frontend
npm install
```

#### Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
cp .env.example .env
```

Edit the `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

#### Run the Frontend

```bash
npm run dev
```

The frontend development server will start at `http://localhost:5173`

## Usage

1. **Access the Application**: Open your browser and navigate to `http://localhost:5173`

2. **Create a New Chat**: Click the "+ New Chat" button in the sidebar

3. **Send Messages**: Type your medical question in the input field and press Enter or click the send button

4. **View Chat History**: All your previous conversations are listed in the sidebar with timestamps

5. **Switch Conversations**: Click on any chat in the sidebar to view and continue that conversation

6. **Delete Chats**: Hover over a chat in the sidebar and click the "×" button to delete it

## API Endpoints

The backend provides the following REST API endpoints:

### Chats

- `POST /api/chats` - Create a new chat
  - Response: Chat object with `id`, `title`, `created_at`, `updated_at`, `messages`

- `GET /api/chats` - Get all chats (for sidebar)
  - Response: Array of chat objects without messages

- `GET /api/chats/{chat_id}` - Get a specific chat with all messages
  - Response: Chat object with all messages

- `DELETE /api/chats/{chat_id}` - Delete a chat
  - Response: Success message

### Messages

- `POST /api/chats/{chat_id}/messages` - Send a message and get LLM response
  - Request body: `{"content": "your message"}`
  - Response: Assistant's message object

## Project Structure

```
medical_llm_UI/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── requirements.txt     # Python dependencies
│   ├── config.py            # Configuration (DB, API keys)
│   ├── models/
│   │   └── chat.py          # Pydantic models
│   ├── routes/
│   │   └── chat.py          # Chat API routes
│   ├── services/
│   │   ├── llm_service.py   # LLM API integration
│   │   └── db_service.py    # MongoDB operations
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── package.json
│   ├── public/
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   ├── main.jsx         # Application entry point
│   │   ├── components/
│   │   │   ├── Sidebar.jsx       # Chat history sidebar
│   │   │   ├── ChatArea.jsx      # Main chat area
│   │   │   ├── MessageList.jsx   # List of messages
│   │   │   ├── MessageInput.jsx  # Input field
│   │   │   └── ChatItem.jsx      # Individual chat in sidebar
│   │   ├── services/
│   │   │   └── api.js            # API calls to backend
│   │   └── styles/
│   │       └── *.css             # Component styles
│   └── .env.example
└── README.md
```

## Key Implementation Details

### Context-Aware Conversations

The application maintains conversation context by:
1. Storing all messages in MongoDB
2. When sending a new message, retrieving the last 4 messages from the conversation
3. Sending these messages along with the system prompt and new user message to the LLM
4. This allows the LLM to provide contextually relevant responses

### Auto-generated Chat Titles

- When a new chat is created, it starts with the title "New Chat"
- After the first user message, the title is automatically updated to the first 50 characters of that message
- This provides meaningful identification for each conversation

### Message Storage Schema

**Chat Document:**
```javascript
{
  _id: ObjectId,
  title: String,
  created_at: DateTime,
  updated_at: DateTime,
  messages: [
    {
      role: String,  // "user" or "assistant"
      content: String,
      timestamp: DateTime
    }
  ]
}
```

## Development

### Backend Development

The backend uses FastAPI with hot-reload enabled. Any changes to Python files will automatically restart the server.

### Frontend Development

The frontend uses Vite's hot module replacement (HMR). Changes to React components will be reflected immediately without full page reload.

## Troubleshooting

### MongoDB Connection Issues

If you can't connect to MongoDB:
1. Ensure MongoDB is running: `mongod --version`
2. Check the connection string in your `.env` file
3. Verify MongoDB is listening on the correct port (default: 27017)

### CORS Errors

If you encounter CORS errors:
1. Ensure the backend is running on port 8000
2. Check that the frontend's `VITE_API_URL` matches the backend URL
3. Verify CORS middleware is properly configured in `backend/main.py`

### LLM API Errors

If the LLM doesn't respond:
1. Verify the API URL and API key in `backend/.env`
2. Check your network connection
3. Look at backend console logs for detailed error messages

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.
