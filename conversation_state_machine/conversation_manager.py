from .dialogue_states.launch_state import LaunchState
from .dialogue_states.weather_discussion_state import WeatherDiscussionState, WeatherDiscussionStateTail
from .dialogue_states.icst_state import ICSTActivityState
from .dialogue_states.goodbye_state import GoodbyeState


class ConversationManager:
    def __init__(self):
        self.states = {
            "LaunchState": LaunchState(),
            "WeatherDiscussionState": WeatherDiscussionState(), 
            "WeatherDiscussionStateTail": WeatherDiscussionStateTail(),
            "ICSTActivityState": ICSTActivityState(),
            "GoodbyeState": GoodbyeState()
        }
        self.initial_state = "LaunchState"
    
    def initate_conversation(self, response_builder, user_utterance, session_data):
        current_state_str = self.initial_state
        current_state_obj = self.states[current_state_str]

        response_text = current_state_obj.get_speech(user_utterance, session_data)
        response_builder = current_state_obj.render_display(response_builder, user_utterance, response_text, session_data)
        
        return response_text, response_builder


    def process_request(self, response_builder, user_utterance, session_data):
        """
        Processes the user's input and manages conversation state transitions.

        1. Retrieves the previous state from session data, defaulting to the initial state if absent.
           Note this previous state was already being processed. 
        2. Given the new utterance from user. process_request will determine the current dialogue state (i.e. what should be the response to the user).

        """
        prev_state_str = session_data.get('dialogue_state', self.initial_state)
        
        # Get the previous state object
        prev_state_obj = self.states[prev_state_str]
        
        # update the current state based on user's input
        print ("previous state: ", prev_state_str)
        current_state_str = prev_state_obj.get_next_state(user_utterance, session_data)
        print ('current state: ', current_state_str)
        current_state_obj = self.states[current_state_str]
        print ('here 2')
        # Process the current state and get the response
        response_text = current_state_obj.get_speech(user_utterance, session_data)
        print ('here3', response_text)
        response_builder = current_state_obj.render_display(response_builder, user_utterance, response_text, session_data)
        print ('here4')
        # Call update_session_data 
        current_state_obj.update_session_data(user_utterance, response_text, session_data)
        
        return response_text, response_builder