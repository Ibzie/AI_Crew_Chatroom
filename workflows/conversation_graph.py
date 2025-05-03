from typing import Dict, Any, List, Optional, TypedDict, Literal
from langgraph.graph import StateGraph, END, START
from config.settings import settings
from config.logging_config import logger
from models.message import Message, MessageRole, ConversationState
from agents import AGENT_MAP
from utils.prompts import get_agent_prompt

def agent_node_factory(agent_type: str):
    """
    Factory function to create agent nodes for the conversation graph
    
    Args:
        agent_type: Type of agent to create node for
        
    Returns:
        Function that processes state for this agent type
    """
    def agent_node(state: ConversationState) -> Dict[str, Any]:
        """Process agent turn in conversation"""
        # Get agent class
        if agent_type not in AGENT_MAP:
            logger.error(f"Unknown agent type: {agent_type}")
            return {"next_speaker": "tech_enthusiast", "turns_remaining": 0}
        
        agent_class = AGENT_MAP[agent_type]
        agent_config = agent_class()
        
        # Log agent thinking
        logger.info(f"{agent_type} is thinking about their response...")
        
        # Get agent prompt
        prompt = get_agent_prompt(agent_type, state.topic, state.messages)
        
        # Get agent response directly using the LLM service
        try:
            from services.llm_service import get_llm
            
            # Get the LLM with agent's temperature
            temp = agent_config.temperature if agent_config.temperature is not None else settings.DEFAULT_TEMPERATURE
            model_name = agent_config.model or settings.DEFAULT_MODEL
            llm = get_llm(model=model_name, temperature=temp)
            
            # Generate a response using direct LLM call
            response = llm.invoke(prompt).content
            
            # Create message object
            agent_role = getattr(MessageRole, agent_type.upper())
            message = Message.agent_message(
                agent_role=agent_role,
                content=response,
                metadata={"agent_type": agent_type}
            )
            
            # Update state
            new_messages = state.messages + [message]
            turns = state.turns_remaining - 1
            
            # Determine next speaker
            agent_order = ["tech_enthusiast", "film_critic", "fitness_coach", "philosopher"]
            current_idx = agent_order.index(agent_type)
            
            # If we have turns remaining, go to next agent
            # Otherwise, use a special marker for no more turns
            if turns > 0:
                next_idx = (current_idx + 1) % len(agent_order)
                next_speaker = agent_order[next_idx]
            else:
                # No more turns left
                next_speaker = "DONE"
            
            logger.info(f"{agent_type} responded: {response[:50]}...")
            logger.info(f"Next speaker: {next_speaker}, Turns remaining: {turns}")
            
            return {
                "messages": new_messages, 
                "next_speaker": next_speaker, 
                "turns_remaining": turns
            }
            
        except Exception as e:
            logger.error(f"Error getting response from {agent_type}: {str(e)}")
            # Even in case of error, return a valid state update
            return {
                "next_speaker": "tech_enthusiast",
                "turns_remaining": 0
            }
    
    return agent_node

def route_next_speaker(state: ConversationState) -> Literal["tech_enthusiast", "film_critic", "fitness_coach", "philosopher", "DONE"]:
    """Route to next speaker based on state"""
    return state.next_speaker

def create_conversation_graph() -> StateGraph:
    """
    Create the conversation workflow graph
    
    Returns:
        Compiled StateGraph for conversation workflow
    """
    # Create graph
    workflow = StateGraph(ConversationState)
    
    # Add nodes for each agent
    workflow.add_node("tech_enthusiast", agent_node_factory("tech_enthusiast"))
    workflow.add_node("film_critic", agent_node_factory("film_critic"))
    workflow.add_node("fitness_coach", agent_node_factory("fitness_coach"))
    workflow.add_node("philosopher", agent_node_factory("philosopher"))
    
    # Set entry point
    workflow.set_entry_point("tech_enthusiast")
    
    # Add conditional edges from each agent
    for agent in ["tech_enthusiast", "film_critic", "fitness_coach", "philosopher"]:
        # Add edges for this agent
        workflow.add_conditional_edges(
            agent,                  # Source node
            route_next_speaker,     # Routing function
            {                       # Mapping of return values to nodes
                "tech_enthusiast": "tech_enthusiast",
                "film_critic": "film_critic",
                "fitness_coach": "fitness_coach", 
                "philosopher": "philosopher",
                "DONE": END         # Special case for ending the conversation
            }
        )
    
    # Compile the graph
    return workflow.compile()