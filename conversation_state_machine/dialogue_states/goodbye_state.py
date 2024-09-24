
from ..base_state import BaseState
from ..ai_agent.agents import GoodbyeAgent 
from ..util import render_document, execute_command, animate_display_change

class GoodbyeState(BaseState):
    def __init__(self):
        self.name = "EndState"
    
    def get_speech(self, user_utterance, session_data):
        prompt = GoodbyeAgent().build_prompt(user_utterance, session_data)
        response = GoodbyeAgent().generate_response_from_llm(prompt)
        return response

    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        apl_document_token = 'background_1' # defined in the LaunchState()
        commands = animate_display_change(
            disappear_element_id="response_text_container",
            new_text_id="title_text",
            new_text=response_text,
            appear_element_id="title_text_container",
        )
        return execute_command(
            response_builder=response_builder,
            token = apl_document_token, 
            commands = commands
        )

    def get_next_state(self, user_utterance, session_data):
        # conversation manager will never call this function. 
        pass
    

    def update_session_data(self, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name
