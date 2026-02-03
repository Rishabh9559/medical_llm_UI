import httpx
from typing import List, Dict
from config import settings

class LLMService:
    def __init__(self):
        self.url = settings.llm_api_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
    
    async def get_completion(self, messages: List[Dict[str, str]]) -> str:
        """
        Get a completion from the LLM API.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            
        Returns:
            The assistant's response content
        """
        try:
            # Always include system message at the start
            system_message = {
                "role": "system",
                "content": "You are a helpful medical assistant."
            }
            
            # Ensure system message is first, then add conversation messages
            formatted_messages = [system_message]
            
            # Add conversation history (exclude system messages from history)
            for msg in messages:
                if msg["role"] != "system":
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.url,
                    json={
                        "model": self.model,
                        "messages": formatted_messages,
                        "temperature": 0.2,
                        "max_tokens": 512
                    },
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Extract the assistant's response
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    return "I apologize, but I couldn't generate a response."
                    
        except httpx.HTTPStatusError as e:
            print(f"LLM API HTTP Error: {e}")
            return "I apologize, but I'm having trouble connecting to the medical assistant service. Please try again later."
        except httpx.RequestError as e:
            print(f"LLM API Request Error: {e}")
            return "I apologize, but I'm having trouble connecting to the medical assistant service. Please try again later."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "An unexpected error occurred. Please try again."

llm_service = LLMService()
