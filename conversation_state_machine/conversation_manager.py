from .states import LaunchState, WeatherDiscussionState, EndState
     
class ConversationManager:
    def __init__(self):
        self.states = {
            "LaunchState": LaunchState(),
            "WeatherDiscussionState": WeatherDiscussionState(), 
            "EndState": EndState()
        }
        self.initial_state = "LaunchState"
    
    def initate_conversation(self, response_builder, user_utterance, session_data):
        current_state_str = self.initial_state
        current_state_obj = self.states[current_state_str]

        speech = current_state_obj.get_speech(user_utterance, session_data)
        response_builder = current_state_obj.render_display(response_builder, user_utterance, session_data)
        
        return speech, response_builder


    def process_request(self, response_builder, user_utterance, session_data):
        prev_state_str = session_data.get('dialogue_state', self.initial_state)
        
        # Get the previous state object
        prev_state_obj = self.states[prev_state_str]
        
        # update the current state based on user's input
        current_state_str = prev_state_obj.get_next_state(user_utterance, session_data)
        current_state_obj = self.states[current_state_str]

        # Call update_session_data 
        current_state_obj.update_session_data(session_data)

        # Process the current state and get the response
        speech = current_state_obj.get_speech(user_utterance, session_data)
        response_builder = current_state_obj.render_display(response_builder, user_utterance, session_data)
        
        return speech, response_builder