from .base_agent import BaseAgent
from . import agent_system_prompt

class YesNoAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = agent_system_prompt.YES_NO_AGENT
    
    def build_prompt(self, user_utterance):
        prompt =[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_utterance}
        ]
        return prompt
    

class WeatherDiscussionAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.system_prompt = agent_system_prompt.WEATHER_DISCUSSION_AGENT
    
    def build_prompt(self, user_utterance, session_data):
        prompt = [
            {"role": "system", "content": self.system_prompt}
        ]
        parsed_conversation = self._parse_conversation_history(session_data['chat_history'])
        prompt.extend(parsed_conversation)
        prompt.append({"role": "user", "content": user_utterance})
        print ("prompt", prompt)
        return prompt
        


