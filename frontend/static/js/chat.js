document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const startChatSection = document.getElementById('startChatSection');
    const chatArea = document.getElementById('chatArea');
    const messagesContainer = document.getElementById('messagesContainer');
    const topicInput = document.getElementById('topicInput');
    const messageInput = document.getElementById('messageInput');
    const startChatBtn = document.getElementById('startChatBtn');
    const sendMessageBtn = document.getElementById('sendMessageBtn');
    
    // State
    let currentConversationId = null;
    let lastMessageCount = 0;
    let isWaitingForAgents = false;
    
    // Event Listeners
    startChatBtn.addEventListener('click', startNewConversation);
    sendMessageBtn.addEventListener('click', sendMessage);
    
    // Allow Enter key to submit
    topicInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') startNewConversation();
    });
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
    
    // Functions
    async function startNewConversation() {
        const topic = topicInput.value.trim();
        if (!topic) {
            alert('Please enter a topic to discuss');
            return;
        }
        
        // Show loading state
        startChatBtn.disabled = true;
        startChatBtn.textContent = 'Starting...';
        
        try {
            // Call API to start conversation
            const response = await fetch('/api/start-conversation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic })
            });
            
            if (!response.ok) throw new Error('Failed to start conversation');
            
            const data = await response.json();
            currentConversationId = data.conversation_id;
            
            // Display initial messages
            displayMessages(data.messages);
            
            // Switch to chat interface
            startChatSection.style.display = 'none';
            chatArea.style.display = 'flex';
            
            // Get AI responses
            await getAgentResponses();
            
        } catch (error) {
            console.error('Error starting conversation:', error);
            alert('Failed to start conversation. Please try again.');
            startChatBtn.disabled = false;
            startChatBtn.textContent = 'Start Chat';
        }
    }
    
    async function sendMessage() {
        if (!currentConversationId) return;
        
        const message = messageInput.value.trim();
        if (!message) {
            alert('Please enter a message');
            return;
        }
        
        // Disable input while sending
        messageInput.disabled = true;
        sendMessageBtn.disabled = true;
        
        try {
            // Add user message to UI immediately
            addMessageToUI({
                role: 'user',
                content: message,
                id: 'temp-' + Date.now()
            });
            
            // Clear input
            messageInput.value = '';
            
            // Call API to add message
            const response = await fetch(`/api/add-message/${currentConversationId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) throw new Error('Failed to send message');
            
            // Get updated messages (including our user message with proper ID)
            const data = await response.json();
            lastMessageCount = data.messages.length;
            
            // Get AI responses
            await getAgentResponses();
            
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message. Please try again.');
        } finally {
            // Re-enable input
            messageInput.disabled = false;
            sendMessageBtn.disabled = false;
            messageInput.focus();
        }
    }
    
    async function getAgentResponses() {
        if (!currentConversationId || isWaitingForAgents) return;
        
        isWaitingForAgents = true;
        
        // Add loading indicator
        const loadingElement = document.createElement('div');
        loadingElement.className = 'loading';
        loadingElement.innerHTML = `
            <div class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        messagesContainer.appendChild(loadingElement);
        
        try {
            // Call API to get agent responses
            const response = await fetch(`/api/continue-conversation/${currentConversationId}`);
            
            if (!response.ok) throw new Error('Failed to get responses');
            
            const data = await response.json();
            
            // Remove loading indicator
            messagesContainer.removeChild(loadingElement);
            
            // Display only new messages
            if (data.messages.length > lastMessageCount) {
                const newMessages = data.messages.slice(lastMessageCount);
                displayMessages(newMessages);
                lastMessageCount = data.messages.length;
            }
            
        } catch (error) {
            console.error('Error getting agent responses:', error);
            // Remove loading indicator on error
            if (messagesContainer.contains(loadingElement)) {
                messagesContainer.removeChild(loadingElement);
            }
        } finally {
            isWaitingForAgents = false;
            // Re-enable input
            messageInput.disabled = false;
            sendMessageBtn.disabled = false;
            messageInput.focus();
        }
    }
    
    function displayMessages(messages) {
        messages.forEach(addMessageToUI);
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    function addMessageToUI(message) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${message.role}`;
        messageElement.dataset.id = message.id;
        
        // Format the role name for display
        let displayRole = message.role.replace('_', ' ');
        displayRole = displayRole.charAt(0).toUpperCase() + displayRole.slice(1);
        
        messageElement.innerHTML = `
            <div class="message-header">${displayRole}</div>
            <div class="message-content">${message.content}</div>
        `;
        
        // Check if this message already exists (for temp messages)
        const existingMsg = document.querySelector(`.message[data-id="temp-${message.id}"]`);
        if (existingMsg) {
            messagesContainer.replaceChild(messageElement, existingMsg);
        } else {
            messagesContainer.appendChild(messageElement);
        }
    }
});