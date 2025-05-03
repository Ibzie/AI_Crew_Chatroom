from typing import List, Dict, Any, Optional, Tuple
from models.message import Message, MessageRole, ConversationState
from workflows.conversation_graph import create_conversation_graph
from utils.memory import ConversationMemory
from config.logging_config import logger
from config.settings import settings

class ChatManager:
    """Manager class for handling multi-agent chat interactions"""
    
    def __init__(self):
        """Initialize the chat manager"""
        self.conversation_graph = create_conversation_graph()
        self.active_conversations: Dict[str, ConversationState] = {}
    
    def start_conversation(self, topic: str, user_message: str, num_turns: int = 4) -> Tuple[str, List[Message]]:
        """
        Start a new conversation
        
        Args:
            topic: Conversation topic
            user_message: Initial user message
            num_turns: Number of agent turns to include
            
        Returns:
            Tuple of (conversation_id, messages)
        """
        # Create initial message
        initial_message = Message.user_message(user_message)
        
        # Create conversation state
        state = ConversationState(
            topic=topic,
            messages=[initial_message],
            next_speaker="tech_enthusiast",  # Always start with tech enthusiast
            turns_remaining=num_turns
        )
        
        # Store in active conversations
        conversation_id = state.conversation_id
        self.active_conversations[conversation_id] = state
        
        # Create memory handler
        memory = ConversationMemory(conversation_id)
        
        # Save initial state
        memory.save_conversation(state.messages, state.metadata)
        
        logger.info(f"Started new conversation {conversation_id} on topic: {topic}")
        
        return conversation_id, state.messages
    
    def continue_conversation(self, conversation_id: str) -> List[Message]:
        """
        Continue an existing conversation for one full round
        
        Args:
            conversation_id: ID of conversation to continue
            
        Returns:
            Updated list of messages
        """
        # Get conversation state
        if conversation_id not in self.active_conversations:
            logger.error(f"Conversation {conversation_id} not found")
            return []
        
        state = self.active_conversations[conversation_id]
        
        # If turns are exhausted, just return the current messages without executing the graph
        if state.turns_remaining <= 0:
            logger.info(f"No more turns remaining for conversation {conversation_id}")
            return state.messages
        
        # Run the conversation graph
        logger.info(f"Continuing conversation {conversation_id}, turns remaining: {state.turns_remaining}")
        
        try:
            # Execute the graph - this will run until all agents have responded or an error occurs
            result = self.conversation_graph.invoke(state)
            
            # Extract the updated messages from the result
            # The graph may return an AddableValuesDict instead of our ConversationState
            if hasattr(result, "messages"):
                # Direct access if it's a ConversationState
                updated_messages = result.messages
            elif isinstance(result, dict) and "messages" in result:
                # Dictionary-like access if it's an AddableValuesDict
                updated_messages = result["messages"]
            else:
                # Fallback to current messages if structure is unexpected
                logger.warning(f"Unexpected result structure: {type(result)}")
                updated_messages = state.messages
            
            # Create a new state object with the updated values
            updated_state = ConversationState(
                topic=state.topic,
                messages=updated_messages,
                next_speaker="tech_enthusiast",  # Reset for next round
                turns_remaining=0,  # Mark as completed round
                conversation_id=state.conversation_id,
                metadata=state.metadata
            )
            
            # Update active conversation state
            self.active_conversations[conversation_id] = updated_state
            
            # Save updated state
            memory = ConversationMemory(conversation_id)
            memory.save_conversation(updated_state.messages, updated_state.metadata)
            
            logger.info(f"Conversation round {conversation_id} completed")
            return updated_messages
            
        except Exception as e:
            logger.error(f"Error continuing conversation: {str(e)}")
            # Return current messages in case of error
            return state.messages
    
    def add_user_message(self, conversation_id: str, message: str) -> List[Message]:
        """
        Add a user message to an existing conversation and reset the turns
        
        Args:
            conversation_id: ID of conversation to add to
            message: User message text
            
        Returns:
            Updated list of messages
        """
        # Get conversation state
        if conversation_id not in self.active_conversations:
            logger.error(f"Conversation {conversation_id} not found")
            return []
        
        state = self.active_conversations[conversation_id]
        
        # Create user message
        user_message = Message.user_message(message)
        
        # Add to state
        updated_messages = state.messages + [user_message]
        
        # Create updated state
        updated_state = ConversationState(
            topic=state.topic,
            messages=updated_messages,
            next_speaker="tech_enthusiast",  # Always start with tech enthusiast after user message
            turns_remaining=4,  # Reset to default number of turns
            conversation_id=state.conversation_id,
            metadata=state.metadata
        )
        
        # Update active conversation state
        self.active_conversations[conversation_id] = updated_state
        
        # Save updated state
        memory = ConversationMemory(conversation_id)
        memory.save_conversation(updated_state.messages, updated_state.metadata)
        
        logger.info(f"Added user message to conversation {conversation_id}")
        
        return updated_messages
    
    def get_conversation(self, conversation_id: str) -> Optional[List[Message]]:
        """
        Get the current state of a conversation
        
        Args:
            conversation_id: ID of conversation to retrieve
            
        Returns:
            List of messages or None if not found
        """
        # Check if in active conversations
        if conversation_id in self.active_conversations:
            state = self.active_conversations[conversation_id]
            if hasattr(state, "messages"):
                return state.messages
            elif isinstance(state, dict) and "messages" in state:
                return state["messages"]
            else:
                logger.warning(f"Unexpected state structure: {type(state)}")
                return []
        
        # Try to load from disk
        memory = ConversationMemory(conversation_id)
        messages, metadata = memory.load_conversation()
        
        if messages:
            # Restore to active conversations if found
            topic = metadata.get("topic", "General Discussion")
            state = ConversationState(
                conversation_id=conversation_id,
                topic=topic,
                messages=messages,
                next_speaker="tech_enthusiast",
                turns_remaining=0,  # Mark as completed
                metadata=metadata
            )
            self.active_conversations[conversation_id] = state
            return messages
        
        return None