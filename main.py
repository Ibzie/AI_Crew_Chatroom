import os
import sys
import argparse
from pathlib import Path

# Add project root to path to ensure imports work
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import settings
from config.logging_config import logger
from workflows.chat_manager import ChatManager
from models.message import MessageRole
from utils.memory import ConversationMemory

def display_message(msg):
    """Format and display a message with appropriate styling"""
    role_display = msg.role.value.replace('_', ' ').title()
    
    # Different styling for different roles
    if msg.role == MessageRole.USER:
        print(f"\n\033[1;36m{role_display}:\033[0m {msg.content}")
    elif msg.role == MessageRole.TECH_ENTHUSIAST:
        print(f"\n\033[1;33m{role_display}:\033[0m {msg.content}")
    elif msg.role == MessageRole.FILM_CRITIC:
        print(f"\n\033[1;35m{role_display}:\033[0m {msg.content}")
    elif msg.role == MessageRole.FITNESS_COACH:
        print(f"\n\033[1;32m{role_display}:\033[0m {msg.content}")
    elif msg.role == MessageRole.PHILOSOPHER:
        print(f"\n\033[1;34m{role_display}:\033[0m {msg.content}")
    else:
        print(f"\n\033[1;37m{role_display}:\033[0m {msg.content}")

# Fixed run_interactive_chat function for main.py

def run_interactive_chat():
    """Run an interactive chat session in the terminal"""
    chat_manager = ChatManager()
    
    print("\n\033[1;37m===== AI Hangout - CrewAI & Langraph Chat =====\033[0m")
    print("\033[0;37mHave a conversation with a group of AI personalities!\033[0m")
    
    # Get conversation topic
    topic = input("\n\033[1;37mWhat would you like to discuss today?\033[0m\n> ")
    
    # Start the conversation
    print("\n\033[0;37mStarting conversation...\033[0m")
    conversation_id, messages = chat_manager.start_conversation(
        topic=topic,
        user_message=f"I'd like to discuss {topic}. What do you think?",
        num_turns=4  # Each agent will respond once in a round
    )
    
    # Display initial user message
    display_message(messages[0])
    
    # Main conversation loop
    while True:
        # Run one round of agent responses
        updated_messages = chat_manager.continue_conversation(conversation_id)
        
        # Display any new agent messages
        new_messages_count = len(updated_messages) - len(messages)
        if new_messages_count > 0:
            for msg in updated_messages[-new_messages_count:]:
                display_message(msg)
        
        # Update our local copy of messages
        messages = updated_messages
        
        # Since we've completed a round, prompt for user input
        user_input = input("\n\033[1;36mYour response (or 'exit' to quit):\033[0m\n> ")
        
        # Check if user wants to exit
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
            
        # Add user message and update local messages
        messages = chat_manager.add_user_message(conversation_id, user_input)
        
    print("\n\033[1;37m===== Conversation Ended =====\033[0m")
    print(f"\033[0;37mConversation saved with ID: {conversation_id}\033[0m")
    
    # Interactive loop
    while True:
        # Get user input
        user_input = input("\n\033[1;36mYour response (or 'exit' to quit):\033[0m\n> ")
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
        
        # Add user message
        chat_manager.add_user_message(conversation_id, user_input)
        
        try:
            # Continue conversation for another round
            updated_messages = chat_manager.continue_conversation(conversation_id)
            
            # Get the most recent messages (the user's message and agent responses)
            user_msg_index = len(messages) 
            messages = updated_messages
            
            # Display all new messages except the user's (which we already showed)
            for msg in updated_messages[user_msg_index + 1:]:
                display_message(msg)
                
        except Exception as e:
            print(f"\n\033[1;31mError continuing conversation: {str(e)}\033[0m")
    
    print("\n\033[1;37m===== Conversation Ended =====\033[0m")
    print(f"\033[0;37mConversation saved with ID: {conversation_id}\033[0m")

def main():
    """Main entry point with command line argument handling"""
    parser = argparse.ArgumentParser(description="AI Hangout - Chat with AI personalities")
    
    # Add arguments
    parser.add_argument("--mode", choices=["interactive", "api"], default="interactive",
                      help="Run in interactive terminal mode or as API server")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check for API key
    if not settings.GROQ_API_KEY:
        print("\033[1;31mError: GROQ_API_KEY environment variable is not set.\033[0m")
        print("Please set it by running:")
        print("  export GROQ_API_KEY=your_api_key")
        print("Or create a .env file with GROQ_API_KEY=your_api_key")
        return
    
    # Run in selected mode
    if args.mode == "interactive":
        run_interactive_chat()
    else:
        # Import here to avoid loading FastAPI unless needed
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        import uvicorn
        
        # Initialize FastAPI
        app = FastAPI(title="AI Hangout API")
        chat_manager = ChatManager()
        
        # Define API models
        class ConversationRequest(BaseModel):
            topic: str
            message: str
            turns: int = 4
        
        class MessageRequest(BaseModel):
            message: str
        
        # API endpoints
        @app.post("/conversations")
        def create_conversation(request: ConversationRequest):
            conversation_id, messages = chat_manager.start_conversation(
                topic=request.topic,
                user_message=request.message,
                num_turns=request.turns
            )
            
            # Process the conversation
            updated_messages = chat_manager.continue_conversation(conversation_id)
            
            return {
                "conversation_id": conversation_id,
                "messages": [msg.to_dict() for msg in updated_messages]
            }
        
        @app.post("/conversations/{conversation_id}/messages")
        def add_message(conversation_id: str, request: MessageRequest):
            # Add user message
            chat_manager.add_user_message(conversation_id, request.message)
            
            # Continue conversation
            updated_messages = chat_manager.continue_conversation(conversation_id)
            
            if not updated_messages:
                raise HTTPException(status_code=404, detail="Conversation not found")
            
            return {
                "messages": [msg.to_dict() for msg in updated_messages]
            }
        
        @app.get("/conversations/{conversation_id}")
        def get_conversation(conversation_id: str):
            messages = chat_manager.get_conversation(conversation_id)
            
            if not messages:
                raise HTTPException(status_code=404, detail="Conversation not found")
            
            return {
                "conversation_id": conversation_id,
                "messages": [msg.to_dict() for msg in messages]
            }
        
        # Start API server
        logger.info(f"Starting API server on {settings.API_HOST}:{settings.API_PORT}")
        uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)

if __name__ == "__main__":
    main()
