import json


class State:
    def get_speech(self, request_json, session_data):
        raise NotImplementedError("Subclasses should implement this method.")
    def get_next_state(self, session_data, request_data):
        raise NotImplementedError("Subclasses should implement this method.")
    
class LaunchState(State):
    def get_speech(self, user_utterance, session_data):
        speech = "Hi, welcome to iCST activity! Do you want to start today's activity? "
        return speech

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if user_utterance == None:
            return "LaunchState"
        elif user_utterance == "yes":
            return "WeatherDiscussionState"
        elif user_utterance == "no":
            return "EndState"
        else:
            return "LaunchState"
    

class WeatherDiscussionState(State):
    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        return "WeatherDiscussionState"
    
    def get_speech(self, next_state, session_data):
        return "hello"

        
class ConversationManager:
    def __init__(self):
        self.states = {
            "LaunchState": LaunchState(),
            "WeatherDiscussionState": WeatherDiscussionState(), 
        }
        self.initial_state = "LaunchState"
    
    def initate_conversation(self, user_utterance, session_data):
        current_state_str = self.initial_state
        current_state_obj = self.states[current_state_str]

        speech = current_state_obj.get_speech(user_utterance, session_data)
        
        return {"speech": speech, "state": current_state_str}


    def process_request(self, user_utterance, session_data):
        prev_state_str = session_data.get('state', self.initial_state)
        
        # Get the previous state object
        prev_state_obj = self.states[prev_state_str]
        
        # update the current state based on user's input
        current_state_str = prev_state_obj.get_next_state(user_utterance, session_data)
        current_state_obj = self.states[current_state_str]

        # Process the current state and get the response
        speech = current_state_obj.get_speech(user_utterance, session_data)
        
        return {"speech": speech, "state": current_state_str}