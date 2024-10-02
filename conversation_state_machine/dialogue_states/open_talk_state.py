import logging
from ..base_state import BaseState
from ..ai_agent.agents import OpenTalkAgent, YesNoAgent
from ..util import render_document, execute_command, animate_display_change, render_document_speakitem
from alexa.util import ChatHistoryLogger

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OpenTalkStateHead(BaseState):
    def __init__(self) -> None:
        self.name = "OpenTalkStateHead"
        self.chat_history_name = "opentalk_chat_history"

    def get_speech(self, user_utterance, session_data):
        response = "Do you want to start a open talk with me? "
        return response
    
    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        return render_document_speakitem(response_builder = response_builder,
                        token = 'background_1',
                        document = "/gui/template_speakitem.json",
                        response_text=response_text
                        )

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        prompt = YesNoAgent().build_prompt(user_utterance)
        response = YesNoAgent().generate_response_from_llm(prompt)
        logger.info('%s %s %s', self.name, 'get_next_state', response)
        if response == "True":
            return "OpenTalkState"
        elif response == "False":
            return "GoodbyeState"
        
    def update_session_data(self, user_utterance, response_text, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name

class OpenTalkState(BaseState):
    def __init__(self) -> None:
        self.name = "OpenTalkState"
        self.chat_history_name = "opentalk_chat_history"
        self.count_var = "opentalk_count"

    def get_speech(self, user_utterance, session_data):
        chat_history = session_data.get(self.chat_history_name, "")
        prompt = OpenTalkAgent().build_prompt(user_utterance, chat_history, state="DISCUSSION")
        response = OpenTalkAgent().generate_response_from_llm(prompt)
        logger.info('%s %s %s', self.name, 'get_speech', response)
        return response
    
    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        apl_document_token = 'background_1' # defined in the LaunchState()
        return render_document_speakitem(response_builder = response_builder,
                        token = 'background_1',
                        document = "/gui/template_speakitem.json",
                        response_text=response_text
                        )

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if session_data.get(self.count_var, 0) >= 3:
            chat_history = session_data.get(self.chat_history_name)
            prompt = OpenTalkAgent().build_prompt(user_utterance, chat_history, state="CHECK_TRANSITION")
            response = OpenTalkAgent().generate_response_from_llm(prompt)
            logger.info('%s %s %s', self.name, 'get_next_state', response)
            if response == "True":
                return "OpenTalkStateTail"
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


class OpenTalkStateTail(BaseState):
    def __init__(self) -> None:
        self.name = "OpenTalkStateTail"
        self.chat_history_name = "opentalk_chat_history"
        self.count_var = "opentalk_count"

    def get_speech(self, user_utterance, session_data):
        chat_history = session_data.get(self.chat_history_name)
        prompt = OpenTalkAgent().build_prompt(user_utterance, chat_history, state="ASK_TRANSITION_QUESTION")
        response = OpenTalkAgent().generate_response_from_llm(prompt)
        return response
    
    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        return render_document_speakitem(response_builder = response_builder,
                        token = 'background_1',
                        document = "/gui/template_speakitem.json",
                        response_text=response_text
                        )

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        prompt = YesNoAgent().build_prompt(user_utterance)
        response = YesNoAgent().generate_response_from_llm(prompt)
        logger.info('%s %s %s', self.name, 'get_next_state', response)
        if response == "True":
            return "ICSTActivityState"
        elif response == "False":
            return "OpenTalkState"
    
    def update_session_data(self, user_utterance, response_text, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name
        session_data[self.count_var] = 0