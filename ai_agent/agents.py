from .base_agent import BaseAgent
from . import agent_system_prompt

class YesNoAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = agent_system_prompt.YES_NO_AGENT
    
    def build_prompt(self, user_utterance):
        system_prompt = self.system_prompt
        human_prompt = user_utterance
        return system_prompt, human_prompt
    
