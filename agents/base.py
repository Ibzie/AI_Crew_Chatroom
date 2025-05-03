from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from crewai import Agent
from config.settings import settings
from services.llm_service import get_llm

class BaseAgentConfig(BaseModel):
    """Base configuration for all agent types"""
    name: str
    role: str
    goal: str
    backstory: str
    verbose: bool = settings.DEFAULT_VERBOSE
    allow_delegation: bool = False
    temperature: Optional[float] = None
    model: Optional[str] = None
    tools: Optional[List[Any]] = None
    
    def create_agent(self) -> Agent:
        """Create a CrewAI agent from this configuration"""
        # Use the specified model or fall back to default
        model_name = self.model or settings.DEFAULT_MODEL
        temp = self.temperature if self.temperature is not None else settings.DEFAULT_TEMPERATURE
        
        # Get LLM with appropriate settings
        llm = get_llm(model=model_name, temperature=temp)
        
        # Create the agent
        return Agent(
            name=self.name,
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=self.verbose,
            allow_delegation=self.allow_delegation,
            llm=llm,
            tools=self.tools or []
        )