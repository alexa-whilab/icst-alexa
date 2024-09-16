class BaseState:
    def get_speech(self, request_json, session_data):
        raise NotImplementedError("Subclasses should implement this method.")
    def get_next_state(self, session_data, request_data):
        raise NotImplementedError("Subclasses should implement this method.")
    def update_session_data(self, session_data):
        raise NotImplementedError("Subclasses should implement this method.")