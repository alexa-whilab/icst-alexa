import json


class State:
    def handle_input(self, request_json, session_data):
        raise NotImplementedError("Subclasses should implement this method.")
    def determine_next_state(self, session_data, request_data):
        raise NotImplementedError("Subclasses should implement this method.")
    
class LaunchState(State):
    def handle_input(self, user_utterance, session_data):
        next_state = self.determine_next_state(user_utterance, session_data)
        speech = self.determine_speech(next_state)
        return {"speech": speech, "next_state": next_state}

    def determine_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if user_utterance == None:
            return "LaunchState"
        elif user_utterance == "yes":
            return "DiscussWeatherState"
        elif user_utterance == "no":
            return "EndState"
        else:
            return "LaunchState"
    
    def determine_speech(self, next_state):
        if next_state == "LaunchState":
            speech = "Hi, welcome to iCST activity! Do you want to start today's activity? "
        elif next_state == "DiscussWeatherState":
            speech = "Let's discuss about today's weather! "
        else:
            speech = "Sorry, I have a trouble processing your request. "
        return speech

class DiscussWeatherState(State):
    def handle_input(self, user_utterance, session_data):
        next_state = self.determine_next_state(user_utterance, session_data)
        speech = self.determine_speech(next_state)
        return {"speech": speech, "next_state": next_state}

    def determine_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        pass
    
    def determine_speech(self, next_state):
        pass

        
class ConversationManager:
    def __init__(self):
        self.states = {
            "LaunchState": LaunchState()
        }
        self.initial_state = "LaunchState"
    
    def initate_conversation(self, user_utterance, session_data):
        dialogue_state = self.initial_state
        state_obj = self.states[dialogue_state]
        result = state_obj.handle_input(user_utterance, session_data)
        return result

    def process_request(self, user_utterance, session_data):
        dialogue_state = session_data.get('dialogue_state', self.initial_state)
        
        # Get the current state object
        state_obj = self.states[dialogue_state]
        
        # Process the input and get the response and next state
        result = state_obj.handle_input(user_utterance, session_data)
        
        return result