
from .base_state import BaseState
from ai_agent.agents import YesNoAgent


class LaunchState(BaseState):
    def __init__(self):
        self.name = "LaunchState"
    def get_speech(self, user_utterance, session_data):
        speech = "Hi, welcome to iCST activity! Do you want to start today's activity? "
        return speech

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition=
        if user_utterance == None:
            return "LaunchState"
        prompt = YesNoAgent().build_prompt(user_utterance)
        response = YesNoAgent().generate_response_from_llm(prompt)
        if response == "True":
            return "WeatherDiscussionState"
        elif response == "False":
            return "EndState"
        else:
            return "LaunchState"
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name

class WeatherDiscussionState(BaseState):
    def __init__(self) -> None:
        self.name = "WeatherDiscussionState"
    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if session_data.get("weather_count", 0) >= 3:
            return "EndState"
        return "WeatherDiscussionState"
    
    def get_speech(self, next_state, session_data):
        return "At Weather Discussion State"
    
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['weather_count'] = session_data.get('weather_count', 0) + 1
        session_data['dialogue_state'] = self.name
    

class EndState(BaseState):
    def __init__(self):
        self.name = "EndState"
    def get_speech(self, user_utterance, session_data):
        speech = "Good bye, see you next time!"
        return speech

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition=
        pass
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name