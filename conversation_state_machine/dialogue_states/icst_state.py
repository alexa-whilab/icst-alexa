
import logging
from ..base_state import BaseState
from ..ai_agent.agents import ICSTActivityAgent, YesNoAgent
from ..util import render_document, execute_command, animate_display_change

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ICSTActivityState(BaseState):
    def __init__(self) -> None:
        self.name = "ICSTActivityState"

    def get_speech(self, user_utterance, session_data):
        prompt = ICSTActivityAgent().build_prompt(user_utterance, session_data, state="DISCUSSION")
        response = ICSTActivityAgent().generate_response_from_llm(prompt)
        logger.info('%s %s %s', self.name, 'get_speech', response)
        return response
    
    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        apl_document_token = 'background_1' # defined in the LaunchState()
        commands = []
        if session_data.get("icst_count",0) == 0:
            commands = animate_display_change(
                appear_element_id="response_text_container",
                new_text_id="response_text",
                new_text="An apple a day keeps the doctor away. "
            )
        return execute_command(
            response_builder=response_builder,
            token = apl_document_token, 
            commands = commands
        )

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if session_data.get("icst_count", 0) >= 1:
            prompt = ICSTActivityAgent().build_prompt(user_utterance, session_data, state="CHECK_TRANSITION")
            response = ICSTActivityAgent().generate_response_from_llm(prompt)
            logger.info('%s %s %s', self.name, 'get_next_state', response)
            if response == "True":
                return "GoodbyeState"
        return self.name
    
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['icst_count'] = session_data.get('icst_count', 0) + 1
        session_data['dialogue_state'] = self.name




    
