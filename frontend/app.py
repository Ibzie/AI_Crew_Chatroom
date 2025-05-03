from flask import Flask, render_template, request, jsonify, session
import uuid
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Now we can import from the main project
from workflows.chat_manager import ChatManager

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize the chat manager
chat_manager = ChatManager()

@app.route('/')
def index():
    """Render the home page"""
    # Set a unique session ID if not already set
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    return render_template('index.html')

@app.route('/api/start-conversation', methods=['POST'])
def start_conversation():
    """Start a new conversation with the AI agents"""
    data = request.json
    topic = data.get('topic', 'General conversation')
    
    # Start a new conversation
    conversation_id, messages = chat_manager.start_conversation(
        topic=topic,
        user_message=f"I'd like to discuss {topic}. What do you think?",
        num_turns=4
    )
    
    # Return the conversation ID and initial messages
    return jsonify({
        'conversation_id': conversation_id,
        'messages': [format_message(msg) for msg in messages]
    })

@app.route('/api/continue-conversation/<conversation_id>', methods=['GET'])
def continue_conversation(conversation_id):
    """Continue the conversation with AI agents responding"""
    # Continue the conversation for one round
    messages = chat_manager.continue_conversation(conversation_id)
    
    # Return the updated messages
    return jsonify({
        'conversation_id': conversation_id,
        'messages': [format_message(msg) for msg in messages]
    })

@app.route('/api/add-message/<conversation_id>', methods=['POST'])
def add_message(conversation_id):
    """Add a user message to the conversation"""
    data = request.json
    message = data.get('message', '')
    
    # Add user message
    messages = chat_manager.add_user_message(conversation_id, message)
    
    # Return the updated messages
    return jsonify({
        'conversation_id': conversation_id,
        'messages': [format_message(msg) for msg in messages]
    })

def format_message(message):
    """Format message object for JSON response"""
    return {
        'id': message.id,
        'role': message.role.value,
        'content': message.content,
        'timestamp': message.timestamp.isoformat() if hasattr(message.timestamp, 'isoformat') else str(message.timestamp)
    }

if __name__ == '__main__':
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)