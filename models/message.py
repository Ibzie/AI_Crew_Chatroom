from pydantic import BaseModel, Field
from typing import Optional, List, Any, Literal, Dict
from enum import Enum
from datetime import datetime
import uuid


class MessageRole(str, Enum):
    USER = "user"
    IBZ = "ibz"
    TECH_ENTHUSIAST = "tech_enthusiast"
    FILM_CRITIC = "film_critic"
    PHILOSOPHER = "philosopher"
    FITNESS_COACH = "fitness_coach"
    SYSTEM = "system"

class Message(BaseModel):
    # Message model for keeping past messages for context later on (maybe)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # maybe add logger here later
    def to_dict(self) -> Dict[str, Any]:
        """Dictionary for API stuff"""
        return {
            "id": self.id,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(), #might need to change format here later
            "metadata": self.metadata
        }
    
    @classmethod
    def user_message(cls, content: str) -> "Message":
        return cls(role=MessageRole.USER, content= content)
    
    @classmethod
    def agent_message(cls, agent_role: MessageRole, content: str, metadata: Optional[Dict[str, Any]] = None) -> "Message":
        return cls(role=agent_role, content= content, metadata= metadata or {})
    
class ConversationState(BaseModel):
    """ Model states to incorporate with Langraph workflow"""

    topic: str
    messages: List[Message] = Field(default_factory=list)
    next_speaker: str
    turns_remaining: int
    conversation_id: str = Field(default_factory=lambda:str(uuid.uuid4()))
    metadata: Dict[str, Any] = Field(default_factory= dict)