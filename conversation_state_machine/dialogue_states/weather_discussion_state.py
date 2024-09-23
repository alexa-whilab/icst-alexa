
import logging
from ..base_state import BaseState
from ..ai_agent.agents import WeatherDiscussionAgent, YesNoAgent
from ..util import render_document, execute_command, animate_display_change

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WeatherDiscussionState(BaseState):
    def __init__(self) -> None:
        self.name = "WeatherDiscussionState"

    def get_speech(self, user_utterance, session_data):
        prompt = WeatherDiscussionAgent().build_prompt(user_utterance, session_data, state="DISCUSSION")
        response = WeatherDiscussionAgent().generate_response_from_llm(prompt)
        logger.info('%s %s %s', self.name, 'get_speech', response)
        return response
    
    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        apl_document_token = 'background_1' # defined in the LaunchState()
        commands = animate_display_change(
            disappear_element_id="title_text_container"
        )
        return execute_command(
            response_builder=response_builder,
            token = apl_document_token, 
            commands = commands
        )

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if session_data.get("weather_count", 0) >= 1:
            prompt = WeatherDiscussionAgent().build_prompt(user_utterance, session_data, state="CHECK_TRANSITION")
            response = WeatherDiscussionAgent().generate_response_from_llm(prompt)
            logger.info('%s %s %s', self.name, 'get_next_state', response)
            if response == "True":
                return "WeatherDiscussionStateTail"
        return "WeatherDiscussionState"
    
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['weather_count'] = session_data.get('weather_count', 0) + 1
        session_data['dialogue_state'] = self.name



class WeatherDiscussionStateTail(BaseState):
    def __init__(self) -> None:
        self.name = "WeatherDiscussionStateTail"

    def get_speech(self, user_utterance, session_data):
        prompt = WeatherDiscussionAgent().build_prompt(user_utterance, session_data, state="ASK_TRANSITION_QUESTION")
        response = WeatherDiscussionAgent().generate_response_from_llm(prompt)
        return response
    
    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        return response_builder

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        prompt = YesNoAgent().build_prompt(user_utterance)
        response = YesNoAgent().generate_response_from_llm(prompt)
        logger.info('%s %s %s', self.name, 'get_next_state', response)
        if response == "True":
            return "CSTDiscussionState"
        elif response == "False":
            return "EndState"
    
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name


    
