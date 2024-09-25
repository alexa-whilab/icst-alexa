
import logging
from ..base_state import BaseState
from ..ai_agent.agents import ICSTActivityAgent, YesNoAgent
from ..util import render_document, execute_command, animate_display_change
from alexa.util import ChatHistoryLogger

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ICSTActivityState(BaseState):
    def __init__(self) -> None:
        self.name = "ICSTActivityState"
        self.chat_history_name = "iCST_chat_history"
        self.count_var = "icst_count"

    def get_speech(self, user_utterance, session_data):
        chat_history = session_data.get(self.chat_history_name, "")
        prompt = ICSTActivityAgent().build_prompt(user_utterance, chat_history, state="DISCUSSION")
        response = ICSTActivityAgent().generate_response_from_llm(prompt)
        logger.info('%s %s %s', self.name, 'get_speech', response)
        return response
    
    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        apl_document_token = 'background_1' # defined in the LaunchState()
        if session_data.get(self.count_var,0) == 0:
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
        return response_builder

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if session_data.get(self.count_var, 0) >= 5:
            chat_history = session_data.get(self.chat_history_name, "")
            prompt = ICSTActivityAgent().build_prompt(user_utterance, chat_history, state="CHECK_TRANSITION")
            response = ICSTActivityAgent().generate_response_from_llm(prompt)
            logger.info('%s %s %s', self.name, 'get_next_state', response)
            if response == "True":
                return "GoodbyeState"
        return self.name

    def _log_dialogue_state_chat_history(self, user_utterance, response_text, session_data):
        chat_history_logger = ChatHistoryLogger(previous_history = session_data.get(self.chat_history_name, ""))
        if self.chat_history_name not in session_data:
            chat_history_logger.append_to_chat_history(bot_response=response_text)
        else:
            chat_history_logger.append_to_chat_history(user_input=user_utterance, 
                                    bot_response=response_text)
        return chat_history_logger.get_chat_history()

    def update_session_data(self, user_utterance, response_text, session_data):
        # Custom update logic
        session_data[self.count_var] = session_data.get(self.count_var, 0) + 1
        session_data['dialogue_state'] = self.name
        session_data[self.chat_history_name] = self._log_dialogue_state_chat_history(user_utterance, response_text, session_data)




    
