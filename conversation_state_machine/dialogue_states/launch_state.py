
from ..base_state import BaseState
from ..ai_agent.agents import YesNoAgent
from ..util import render_document, execute_command


class LaunchState(BaseState):
    def __init__(self):
        self.name = "LaunchState"
    
    def get_speech(self, user_utterance=None, session_data=None):
        speech = "Hi, welcome to iCST activity! Do you want to start today's activity? "
        return speech

    def render_display(self, response_builder, user_utterance=None, session_data=None):
        return render_document(response_builder = response_builder,
                               document = "/gui/greeting.json")

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
