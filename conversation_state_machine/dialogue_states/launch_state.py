
import logging
from ..base_state import BaseState
from ..ai_agent.agents import YesNoAgent
from ..util import render_document, execute_command

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchState(BaseState):
    def __init__(self):
        self.name = "LaunchState"
    
    def get_speech(self, user_utterance=None, session_data=None):
        response_text = "Hi, welcome to iCST activity! Do you want to start today's activity? "
        return response_text

    def render_display(self, response_builder, user_utterance=None, response_text=None, session_data=None):
        return render_document(response_builder = response_builder,
                               token = 'background_1',
                               document = "/gui/greeting.json",
                               datasources={
                                   "LambdaData":{
                                       "titleText": "Welcome to iCST Practice!!",
                                   }
                                   }
                               )
    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition=
        if user_utterance == None:
            return "LaunchState"
        prompt = YesNoAgent().build_prompt(user_utterance)
        response = YesNoAgent().generate_response_from_llm(prompt)
        logger.info('%s %s %s', self.name, 'get_next_state', response)
        if response == "True":
            return "WeatherDiscussionState"
        elif response == "False":
            return "GoodbyeState"
        else:
            return "LaunchState"
    
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name
