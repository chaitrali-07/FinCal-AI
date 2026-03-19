"""
Pydantic schemas for AI financial assistant.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class MessageEntry(BaseModel):
    """Represents a single message in conversation history"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class AssistantRequest(BaseModel):
    """Request schema for financial assistant"""
    message: str = Field(..., min_length=1, max_length=2000, description="User's question or message")
    conversation_history: Optional[List[MessageEntry]] = Field(
        default=None,
        description="Previous conversation messages for context"
    )


class AssistantResponse(BaseModel):
    """Response schema for financial assistant"""
    reply: str = Field(..., description="AI assistant's response")
    message_id: str = Field(..., description="Unique message identifier")
    timestamp: str = Field(..., description="Response timestamp")
    success: bool = Field(default=True, description="Whether the request was successful")
    error: Optional[str] = Field(default=None, description="Error message if request failed")


class AssistantError(BaseModel):
    """Error response for assistant"""
    detail: str = Field(..., description="Error description")
    message_id: Optional[str] = Field(default=None, description="Request message ID if available")
