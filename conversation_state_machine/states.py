
from .base_state import BaseState
from ai_agent.agents import YesNoAgent


class LaunchState(BaseState):
    def get_speech(self, user_utterance, session_data):
        speech = "Hi, welcome to iCST activity! Do you want to start today's activity? "
        return speech

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition=
        if user_utterance == None:
            return "LaunchState"
        system_prompt, human_prompt = YesNoAgent().build_prompt(user_utterance)
        response = YesNoAgent().generate_response_from_llm(system_prompt, human_prompt)
        if response == "True":
            return "WeatherDiscussionState"
        elif response == "False":
            return "EndState"
        else:
            return "LaunchState"
    

class WeatherDiscussionState(BaseState):
    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        return "WeatherDiscussionState"
    
    def get_speech(self, next_state, session_data):
        return "hello"