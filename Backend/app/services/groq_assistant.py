import os
from typing import List, Dict, Optional
from datetime import datetime

from groq import Groq

class GroqFinancialAssistant:
    """
    AI Financial Assistant using Groq
    (Advice only – no calculations)
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment")

        self.client = Groq(api_key=api_key)

        self.system_prompt = (
            "You are a financial education assistant. "
            "You give clear, simple financial advice. "
            "You do NOT perform calculations. "
            "You explain concepts like EMI, SIP, tax planning, "
            "investments, and personal finance in simple terms. "
            "Avoid giving legal or investment guarantees."
        )

        print("[OK] Groq AI Assistant initialized")

    def get_response(
        self,
        user_message: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, str]:

        messages = [{"role": "system", "content": self.system_prompt}]

        if chat_history:
            for item in chat_history:
                messages.append({
                    "role": item.get("role", "user"),
                    "content": item.get("content", "")
                })

        messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",   # Very good for advice
            messages=messages,
            temperature=0.4,
            max_tokens=500
        )

        return {
            "response": response.choices[0].message.content,
            "timestamp": datetime.utcnow().isoformat()
        }


_assistant_instance = None

def get_groq_assistant() -> GroqFinancialAssistant:
    global _assistant_instance
    if _assistant_instance is None:
        _assistant_instance = GroqFinancialAssistant()
    return _assistant_instance