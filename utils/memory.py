from typing import List, Dict, Any, Optional
from models.message import Message, MessageRole
from config.settings import settings
import json
import os
from pathlib import Path

class ConversationMemory:
    """Class for managing conversation history persistence"""
    
    def __init__(self, conversation_id: str, storage_dir: Optional[Path] = None):
        self.conversation_id = conversation_id
        self.storage_dir = storage_dir or settings.BASE_DIR / "data" / "conversations"
        self.file_path = self.storage_dir / f"{conversation_id}.json"
        
        # Ensure storage directory exists
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def save_conversation(self, messages: List[Message], metadata: Dict[str, Any]) -> None:
        """Save conversation history to disk"""
        # Convert messages to serializable format
        serialized_messages = [msg.to_dict() for msg in messages]
        
        # Create data structure
        data = {
            "conversation_id": self.conversation_id,
            "messages": serialized_messages,
            "metadata": metadata
        }
        
        # Write to file
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_conversation(self) -> tuple[List[Message], Dict[str, Any]]:
        """Load conversation history from disk"""
        if not os.path.exists(self.file_path):
            return [], {}
        
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        # Convert serialized messages back to Message objects
        messages = []
        for msg_data in data.get("messages", []):
            # Convert string role back to MessageRole enum
            role = MessageRole(msg_data["role"])
            
            # Create Message object
            message = Message(
                id=msg_data["id"],
                role=role,
                content=msg_data["content"],
                timestamp=msg_data["timestamp"],
                metadata=msg_data.get("metadata", {})
            )
            messages.append(message)
        
        return messages, data.get("metadata", {})