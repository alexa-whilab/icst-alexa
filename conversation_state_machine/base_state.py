class BaseState:
    def get_speech(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")
    def get_next_state(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")
    def update_session_data(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")