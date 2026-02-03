from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from config import settings

class DatabaseService:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(settings.mongodb_url)
        self.db = self.client[settings.database_name]
        
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
    
    async def create_chat(self, title: str) -> str:
        """Create a new chat and return its ID"""
        chat_doc = {
            "title": title,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "messages": []
        }
        result = await self.db.chats.insert_one(chat_doc)
        return str(result.inserted_id)
    
    async def get_all_chats(self) -> List[dict]:
        """Get all chats (without messages for efficiency)"""
        chats = []
        cursor = self.db.chats.find({}, {"messages": 0}).sort("updated_at", -1)
        async for chat in cursor:
            chat["id"] = str(chat.pop("_id"))
            chats.append(chat)
        return chats
    
    async def get_chat(self, chat_id: str) -> Optional[dict]:
        """Get a specific chat with all messages"""
        try:
            chat = await self.db.chats.find_one({"_id": ObjectId(chat_id)})
            if chat:
                chat["id"] = str(chat.pop("_id"))
            return chat
        except Exception:
            return None
    
    async def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat"""
        try:
            result = await self.db.chats.delete_one({"_id": ObjectId(chat_id)})
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
