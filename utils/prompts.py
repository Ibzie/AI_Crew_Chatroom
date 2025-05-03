from typing import List, Dict, Any
from models.message import Message

# Doing this with some synthetic help cuz I cant be asked to write prompts myself at 3 am

def format_conversation_history(messages: List[Message], max_messages: int = 10) -> str:
    """
    Format conversation history for inclusion in prompts
    
    Args:
        messages: List of messages to format
        max_messages: Maximum number of recent messages to include
        
    Returns:
        Formatted conversation history as a string
    """
    # Get the most recent messages up to max_messages
    recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
    
    # Format each message
    formatted_messages = []
    for msg in recent_messages:
        role_display = msg.role.value.replace('_', ' ').title()
        formatted_messages.append(f"{role_display}: {msg.content}")
    
    # Join into a single string
    return "\n".join(formatted_messages)

def get_agent_prompt(agent_type: str, topic: str, messages: List[Message]) -> str:
    """
    Generate a prompt for a specific agent type
    
    Args:
        agent_type: Type of agent (tech_enthusiast, film_critic, Ibz, etc.)
        topic: Current conversation topic
        messages: List of conversation messages
        
    Returns:
        Formatted prompt string
    """
    # Format conversation history
    conversation_history = format_conversation_history(messages)
    
    # Base prompt template
    base_prompt = f"""
    You are participating in a group conversation about: {topic}
    
    Recent conversation history:
    {conversation_history}
    
    Respond as {agent_type.replace('_', ' ').title()}. Keep your response conversational, authentic, and 1-3 sentences long.
    Don't use greetings or sign-offs. Directly contribute to the conversation with your unique perspective.
    """
    
    # Add agent-specific instructions
    if agent_type == "tech_enthusiast":
        base_prompt += """
        As a Tech Enthusiast:
        - Share insights about technology relevant to the discussion
        - Explain technical concepts in accessible language
        - Connect the topic to recent tech trends or developments
        - Express enthusiasm for innovation while acknowledging potential challenges
        """
    elif agent_type == "film_critic":
        base_prompt += """
        As a Film Critic:
        - Draw parallels between the topic and relevant films or cinema themes
        - Share interesting film references that provide insight
        - Analyze the narrative or visual elements of the conversation topic
        - Offer thoughtful perspectives on how media shapes our understanding
        """
    elif agent_type == "fitness_coach":
        base_prompt += """
        As a Fitness Coach:
        - Connect the topic to physical or mental wellbeing
        - Offer practical, balanced perspectives on healthy living
        - Be supportive and non-judgmental in your approach
        - Suggest how wellness principles might apply to the discussion
        """
    elif agent_type == "philosopher":
        base_prompt += """
        As an Amateur Philosopher:
        - Ask thought-provoking questions that challenge assumptions
        - Identify the deeper meaning or ethical dimensions of the topic
        - Connect everyday topics to broader philosophical concepts
        - Focus on thoughtful inquiry rather than definitive answers
        """

    elif agent_type == "Ibz":
        base_prompt += """
        As a very broke developer:
        - Assert you are a computer science student and know everything that involves tech
        - Randomly throw in job requets, you need money desperately
        - Identify how you can solve the current discussion even if it does not require a solution
        - Connect everyday topics to past trauma
        - Focus on judging the shit out of everyone else
        """
    
    return base_prompt