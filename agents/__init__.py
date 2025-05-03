from agents.base import BaseAgentConfig
from agents.tech_enthusiast import TechEnthusiast
from agents.film_critic import FilmCritic
from agents.fitness_coach import FitnessCoach
from agents.philosopher import Philosopher

# Dictionary for easy access to agent classes by name
AGENT_MAP = {
    "tech_enthusiast": TechEnthusiast,
    "film_critic": FilmCritic,
    "fitness_coach": FitnessCoach,
    "philosopher": Philosopher
}