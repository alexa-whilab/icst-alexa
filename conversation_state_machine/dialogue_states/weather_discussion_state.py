
from ..base_state import BaseState
from ..ai_agent.agents import WeatherDiscussionAgent
from ..util import render_document, execute_command, animate_display_change


class WeatherDiscussionState(BaseState):
    def __init__(self) -> None:
        self.name = "WeatherDiscussionState"

    def get_speech(self, user_utterance, session_data):
        prompt = WeatherDiscussionAgent().build_prompt(user_utterance, session_data)
        response = WeatherDiscussionAgent().generate_response_from_llm(prompt)
        return response
    
    def render_display(self, response_builder, user_utterance, response_text, session_data=None):
        apl_document_token = 'background_1' # defined in the LaunchState()
        if session_data.get('weather_count', 0) == 0:
            commands = animate_display_change(
                disappear_element_id="title_text_container",
                appear_element_id="response_text_container",
                new_text_id="response_text",
                new_text=response_text,
                speak_item=True
            )
        else:
            commands = animate_display_change(
                disappear_element_id="response_text_container",
                appear_element_id="response_text_container",
                new_text_id="response_text",
                new_text=response_text,
                speak_item=True
            )
        return execute_command(
            response_builder=response_builder,
            token = apl_document_token, 
            commands = commands
        )

    def get_next_state(self, user_utterance, session_data):
        # Custom logic: if session_data or user_input triggers a condition
        if session_data.get("weather_count", 0) >= 3:
            return "EndState"
        return "WeatherDiscussionState"
    
    def update_session_data(self, session_data):
        # Custom update logic
        session_data['weather_count'] = session_data.get('weather_count', 0) + 1
        session_data['dialogue_state'] = self.name
    
