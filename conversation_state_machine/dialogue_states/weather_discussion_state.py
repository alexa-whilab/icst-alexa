
import logging
from ..base_state import BaseState
from ..ai_agent.agents import WeatherDiscussionAgent, YesNoAgent
from ..util import render_document, execute_command, animate_display_change
from alexa.util import ChatHistoryLogger

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WeatherDiscussionState(BaseState):
    def __init__(self) -> None:
        self.name = "WeatherDiscussionState"
        self.chat_history_name = "weather_chat_history"
        self.count_var = "weather_count"

    def get_speech(self, user_utterance, session_data):
        chat_history = session_data.get(self.chat_history_name, "")
        prompt = WeatherDiscussionAgent().build_prompt(user_utterance, chat_history, state="DISCUSSION")
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
        if session_data.get(self.count_var, 0) >= 3:
            chat_history = session_data.get(self.chat_history_name)
            prompt = WeatherDiscussionAgent().build_prompt(user_utterance, chat_history, state="CHECK_TRANSITION")
            response = WeatherDiscussionAgent().generate_response_from_llm(prompt)
            logger.info('%s %s %s', self.name, 'get_next_state', response)
            if response == "True":
                return "WeatherDiscussionStateTail"
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



class WeatherDiscussionStateTail(BaseState):
    def __init__(self) -> None:
        self.name = "WeatherDiscussionStateTail"
        self.chat_history_name = "weather_chat_history"

    def get_speech(self, user_utterance, session_data):
        chat_history = session_data.get(self.chat_history_name)
        prompt = WeatherDiscussionAgent().build_prompt(user_utterance, chat_history, state="ASK_TRANSITION_QUESTION")
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
            return "ICSTActivityState"
        elif response == "False":
            return "GoodbyeState"
    
    def update_session_data(self, user_utterance, response_text, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name


    
