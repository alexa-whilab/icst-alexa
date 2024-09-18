
from ..base_state import BaseState
from ..util import render_document, execute_command

class EndState(BaseState):
    def __init__(self):
        self.name = "EndState"
    
    def get_speech(self, user_utterance, session_data):
        speech = "Good bye, see you next time!"
        return speech

    def get_next_state(self, user_utterance, session_data):
        # conversation manager will never call this function. 
        pass
    
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['dialogue_state'] = self.name