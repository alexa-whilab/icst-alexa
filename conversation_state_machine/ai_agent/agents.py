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
    
    def build_prompt(self, user_utterance, session_data, state):
        self.system_prompt = agent_system_prompt.WEATHER_DISCUSSION_AGENT[state]
        prompt = [
            {"role": "system", "content": self.system_prompt}
        ]
        parsed_conversation = self._parse_conversation_history(session_data.get('weather_chat_history', ""))
        prompt.extend(parsed_conversation)
        if "weather_chat_history" in session_data:
            prompt.append({"role": "user", "content": user_utterance})
        print ("prompt", prompt)
        return prompt
        

class ICSTActivityAgent(BaseAgent):
    def __init__(self):
        super().__init__()
    
    def build_prompt(self, user_utterance, session_data, state):
        self.system_prompt = agent_system_prompt.ICST_ACTIVITY_AGENT[state]
        prompt = [
            {"role": "system", "content": self.system_prompt}
        ]
        parsed_conversation = self._parse_conversation_history(session_data.get('iCST_chat_history', ""))
        prompt.extend(parsed_conversation)
        if "iCST_chat_history" in session_data:
            prompt.append({"role": "user", "content": user_utterance})
        print ("prompt", prompt)
        return prompt
    
class GoodbyeAgent(BaseAgent):
    def __init__(self):
        super().__init__()
    
    def build_prompt(self, user_utterance, session_data):
        self.system_prompt = agent_system_prompt.GOODBYE_AGENT
        prompt = [
            {"role": "system", "content": self.system_prompt}
        ]
        user_prompt = session_data['chat_history'] + "user:" + user_utterance
        prompt.append({"role": "user", "content": user_prompt})
        print ("prompt", prompt)
        return prompt
