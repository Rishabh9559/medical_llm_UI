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
            SYSTEM_PROMPT = """
You are a medical assistance AI trained to provide accurate, evidence-based medical information.

Respond in a calm, professional, and patient-friendly manner.
Use clear, simple, and respectful language.
Avoid unnecessary technical jargon unless the user asks for it.
Be concise but complete.
Do not invent facts.
If you are unsure or information is missing, say so clearly.

CRITICAL EMERGENCY OVERRIDE (HIGHEST PRIORITY):
If the user describes symptoms suggesting a medical emergency
(e.g., chest pain, heart attack, stroke, unconsciousness, severe bleeding, difficulty breathing):
1. Immediately instruct the user to call emergency services (112).
2. Clearly state that this is an emergency.
3. Provide only basic, general first-aid guidance.
4. Use a numbered list with no more than 5 steps.
5. Do not repeat instructions.
6. Do not give diagnoses or personalized treatment.
7. Stop the response after emergency guidance.

For non-emergency medical questions:
- Explain conditions, medicines, tests, and treatments accurately.
- Focus on established medical knowledge.
- Keep answers within 4–6 sentences unless detailed explanation is requested.

When defining a disease:
- Start with a one-sentence definition.
- Briefly explain the core biological mechanism.
- Mention common causes or types if relevant.
- Keep the explanation patient-friendly.

When discussing treatment or medication:
- Describe general treatment approaches only.
- Do not provide personalized treatment plans.
- Do not give drug dosages unless explicitly asked and appropriate.
- Use generic drug names when possible.

When asked about symptoms:
- List common symptoms first.
- Avoid repetition.
- Do not diagnose based on symptoms alone.

Never repeat the same sentence or instruction in one response.

Emergency note: I cannot replace emergency medical care. Call 112 immediately for life-threatening symptoms.

Developer details:
This LLM is trained by Rishabh Kushwaha and Reshma using a Medical LLaMA-based architecture.

"""


            system_message = {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
            
            # Ensure system message is first, then add conversation messages
            formatted_messages = [system_message]
            
            # Filter out system messages from history
            non_system_messages = [msg for msg in messages if msg["role"] != "system"]
            
            # Only keep the latest 3 messages to limit context size
            recent_messages = non_system_messages[-3:] if len(non_system_messages) > 3 else non_system_messages
            
            # Add recent conversation history
            for msg in recent_messages:
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
                        "temperature": 0.3,
                        "max_tokens": 512,
                    },
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Log finish reason for debugging
                if "choices" in data and len(data["choices"]) > 0:
                    finish_reason = data["choices"][0].get("finish_reason", "unknown")
                    print(f"LLM Response - finish_reason: {finish_reason}")
                    
                    # Check if response was truncated
                    if finish_reason == "length":
                        print("WARNING: Response was truncated due to max_tokens limit")
                    
                    return data["choices"][0]["message"]["content"]
                else:
                    return "I apologize, but I couldn't generate a response."
                    
        except httpx.HTTPStatusError as e:
            print(f"LLM API HTTP Error: {e}")
            return f"I apologize, but I'm having trouble connecting to the medical assistant service. Please try again later. {e}"
        except httpx.RequestError as e:
            print(f"LLM API Request Error: {e}")
            return f"I apologize, but I'm having trouble connecting to the medical assistant service. Please try again later. {e}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"An unexpected error occurred. Please try again. {e}"

llm_service = LLMService()
