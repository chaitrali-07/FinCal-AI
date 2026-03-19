"""
FastAPI routes for AI Financial Assistant.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import uuid
from datetime import datetime

from app.schemas.assistant_schema import AssistantRequest, AssistantResponse

try:
   from app.services.groq_assistant import get_groq_assistant
except ImportError as e:
    print(f" Warning: Could not import Groq assistant: {e}")
    get_groq_assistant = None

router = APIRouter(prefix="/api/assistant", tags=["AI Financial Assistant"])


@router.post("/chat", response_model=AssistantResponse)
async def financial_assistant_chat(request: AssistantRequest) -> Dict[str, Any]:
    """Get financial education from AI assistant."""
    message_id = str(uuid.uuid4())
    
    try:
        # Check if Gemini assistant available
        if get_groq_assistant is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Groq not configured. Install: pip install groq"
            )
        
        # Validate message
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )
        
        if len(request.message) > 2000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message too long (max 2000 chars)"
            )
        
        # Get assistant instance
        assistant = get_groq_assistant()

        
        # Format conversation history
        history = None
        if request.conversation_history:
            history = [
                {"role": h.role, "content": h.content}
                for h in request.conversation_history
            ]
        
        # Get response from Gemini
        response_data =  assistant.get_response(
            user_message=request.message,
            chat_history=history
        )
        
        return AssistantResponse(
            reply=response_data["response"],
            message_id=message_id,
            timestamp=response_data["timestamp"],
            success=True
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"[v0] Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


@router.get("/health")
async def assistant_health_check() -> Dict[str, Any]:
    """Check Groq assistant health."""
    try:
        _ = get_groq_assistant()
        return {
            "status": "healthy",
            "message": "Groq Assistant ready",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Gemini error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
