from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from config import settings

class DatabaseService:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self._indexes_created = False
        
    async def connect(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(
            settings.mongodb_url,
            tls=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=30000,  # Increased timeout
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            retryWrites=True,
            retryReads=True,
            maxPoolSize=10,
            minPoolSize=1
        )
        self.db = self.client[settings.database_name]
        
    async def _ensure_indexes(self):
        """Create indexes if not already created"""
        if not self._indexes_created:
            try:
                await self.db.users.create_index("email", unique=True)
                self._indexes_created = True
            except Exception as e:
                print(f"Warning: Could not create indexes: {e}")
        
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
    
    # ============ User Operations ============
    
    async def create_user(self, email: str, name: str, hashed_password: str) -> str:
        """Create a new user and return their ID"""
        user_doc = {
            "email": email,
            "name": name,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow()
        }
        result = await self.db.users.insert_one(user_doc)
        return str(result.inserted_id)
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get a user by email"""
        user = await self.db.users.find_one({"email": email})
        if user:
            user["id"] = str(user.pop("_id"))
        return user
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get a user by ID"""
        try:
            user = await self.db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user.pop("_id"))
            return user
        except Exception:
            return None
    
    # ============ Chat Operations ============
    
    async def create_chat(self, title: str, user_id: str) -> str:
        """Create a new chat and return its ID"""
        chat_doc = {
            "title": title,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "messages": []
        }
        result = await self.db.chats.insert_one(chat_doc)
        return str(result.inserted_id)
    
    async def get_all_chats(self, user_id: str) -> List[dict]:
        """Get all chats for a specific user (without messages for efficiency)"""
        chats = []
        cursor = self.db.chats.find(
            {"user_id": user_id}, 
            {"messages": 0}
        ).sort("updated_at", -1)
        async for chat in cursor:
            chat["id"] = str(chat.pop("_id"))
            chats.append(chat)
        return chats
    
    async def get_chat(self, chat_id: str, user_id: str = None) -> Optional[dict]:
        """Get a specific chat with all messages"""
        try:
            query = {"_id": ObjectId(chat_id)}
            if user_id:
                query["user_id"] = user_id
            chat = await self.db.chats.find_one(query)
            if chat:
                chat["id"] = str(chat.pop("_id"))
            return chat
        except Exception:
            return None
    
    async def delete_chat(self, chat_id: str, user_id: str) -> bool:
        """Delete a chat (only if owned by user)"""
        try:
            result = await self.db.chats.delete_one({
                "_id": ObjectId(chat_id),
                "user_id": user_id
            })
            return result.deleted_count > 0
        except Exception:
            return False
    
    async def add_message(self, chat_id: str, role: str, content: str) -> bool:
        """Add a message to a chat"""
        try:
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow()
            }
            result = await self.db.chats.update_one(
                {"_id": ObjectId(chat_id)},
                {
                    "$push": {"messages": message},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    async def update_chat_title(self, chat_id: str, title: str) -> bool:
        """Update the title of a chat"""
        try:
            result = await self.db.chats.update_one(
                {"_id": ObjectId(chat_id)},
                {"$set": {"title": title, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    async def get_recent_messages(self, chat_id: str, count: int = 4) -> List[dict]:
        """Get the last N messages from a chat"""
        try:
            chat = await self.db.chats.find_one(
                {"_id": ObjectId(chat_id)},
                {"messages": {"$slice": -count}}
            )
            return chat.get("messages", []) if chat else []
        except Exception:
            return []

db_service = DatabaseService()
