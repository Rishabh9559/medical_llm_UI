from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.chat import (
    ChatResponse, ChatListItem, MessageRequest, 
    MessageResponse, Message
)
from models.user import TokenData
from services.db_service import db_service
from services.llm_service import llm_service
from services.auth_service import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/chats", tags=["chats"])

@router.post("", response_model=ChatResponse)
async def create_chat(current_user: TokenData = Depends(get_current_user)):
    """Create a new chat for the authenticated user"""
    # Start with a default title, will be updated with first message
    chat_id = await db_service.create_chat("New Chat", current_user.user_id)
    chat = await db_service.get_chat(chat_id, current_user.user_id)
    
    if not chat:
        raise HTTPException(status_code=500, detail="Failed to create chat")
    
    return ChatResponse(**chat)

@router.get("", response_model=List[ChatListItem])
async def get_all_chats(current_user: TokenData = Depends(get_current_user)):
    """Get all chats for the authenticated user (for sidebar)"""
    chats = await db_service.get_all_chats(current_user.user_id)
    return [ChatListItem(**chat) for chat in chats]

@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: str, current_user: TokenData = Depends(get_current_user)):
    """Get a specific chat with all messages (only if owned by user)"""
    chat = await db_service.get_chat(chat_id, current_user.user_id)
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return ChatResponse(**chat)

@router.delete("/{chat_id}")
async def delete_chat(chat_id: str, current_user: TokenData = Depends(get_current_user)):
    """Delete a chat (only if owned by user)"""
    success = await db_service.delete_chat(chat_id, current_user.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return {"message": "Chat deleted successfully"}

@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message(
    chat_id: str, 
    message: MessageRequest, 
    current_user: TokenData = Depends(get_current_user)
):
    """Send a message and get LLM response"""
    # Verify chat exists and belongs to user
    chat = await db_service.get_chat(chat_id, current_user.user_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Save user message
    await db_service.add_message(chat_id, "user", message.content)
    
    # Update chat title if this is the first message
    if len(chat.get("messages", [])) == 0:
        # Use first 50 chars of message as title
        title = message.content[:50] + "..." if len(message.content) > 50 else message.content
        await db_service.update_chat_title(chat_id, title)
    
    # Get last 4 messages for context
    recent_messages = await db_service.get_recent_messages(chat_id, count=4)
    
    # Format messages for LLM
    formatted_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in recent_messages
    ]
    
    # Add current message if not already in recent messages
    if not formatted_messages or formatted_messages[-1]["content"] != message.content:
        formatted_messages.append({"role": "user", "content": message.content})
    
    # Get LLM response
    assistant_response = await llm_service.get_completion(formatted_messages)
    
    # Save assistant message
    await db_service.add_message(chat_id, "assistant", assistant_response)
    
    return MessageResponse(
        role="assistant",
        content=assistant_response,
        timestamp=datetime.utcnow()
    )
