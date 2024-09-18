
from ..base_state import BaseState
from ..ai_agent.agents import WeatherDiscussionAgent
from ..util import render_document, execute_command


class WeatherDiscussionState(BaseState):
    def __init__(self) -> None:
        self.name = "WeatherDiscussionState"

    def get_speech(self, user_utterance, session_data):
        prompt = WeatherDiscussionAgent().build_prompt(user_utterance, session_data)
        response = WeatherDiscussionAgent().generate_response_from_llm(prompt)
        return response
    
    def get_display(self, response_builder, user_utterance, session_data=None):
        pass

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if session_data.get("weather_count", 0) >= 3:
            return "EndState"
        return "WeatherDiscussionState"
    
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['weather_count'] = session_data.get('weather_count', 0) + 1
        session_data['dialogue_state'] = self.name
    
