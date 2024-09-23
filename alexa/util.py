# -*- coding: utf-8 -*-
import random

from . import data
from typing import Dict

from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective)

def load_locale_specific_recipe(locale):
    """Return the recipe dictionary specific to the locale.

    Checks for a recipe dictionary with name 'RECIPE_<locale>' in data
    module and return it. Returns None if there is no dictionary
    specific to the locale.
    eg: load_locale_specific_recipe('en-US') -> data.RECIPE_EN_US
    """
    # type: (str) -> Dict[str, str]
    return getattr(
        data, "RECIPE_{}".format(locale).upper().replace("-", "_"), None)


def get_random_item(locale):
    """Return a random item from the locale specific dict."""
    # type: (str) -> str
    return random.choice(list(load_locale_specific_recipe(locale).keys()))


def get_user_utterance(handler_input):
    try:
        # Attempt to get the intent and slot value
        return handler_input.request_envelope.request.intent.slots["CatchAll"].value
    except:
        # otherwise return None
        return None 

def get_session_data(handler_input):
    return handler_input.attributes_manager.session_attributes



class ChatHistoryLogger:
    def __init__(self, previous_history=""):
        # Initialize the chat history with an optional previous history
        self.chat_history = previous_history

    def append_to_chat_history(self, user_input=None, bot_response=None):
        # Append the formatted user input and bot response to the chat history
        if user_input == None:
            self.chat_history += f"assistant:{bot_response}|"
        elif bot_response == None:
            self.chat_history += f"user:{user_input}|"
        else:
            self.chat_history += f"user:{user_input}|assistant:{bot_response}|"

    def get_chat_history(self):
        # Return the stored chat history
        return self.chat_history
    

def contains_apl_speak_item(response_builder):
    # Recursive function to check for 'SpeakItem' in the directives
    '''
    the command format must be
    [{
        "type": "Sequential",
        "commands": [
            {
            }
        ]
    ]
    
    In other words, there must be a wrapper outside the series of 
    commands. However, it does not always have to be Sequential. 
    
    '''
    def contains_speak_item(directive):
        command_groups = getattr(directive, "commands", None)
        if not command_groups:
            return False
        for command_group in command_groups:
            commands = command_group.get('commands', None)
            if commands:
                for command in commands:
                    print ('here3', command)
                    if command.get('type') == 'SpeakItem':
                        return True
            return False
    
    # Check each directive in the response
    response = getattr(response_builder, 'response', None)

    # Check if the response has directives, and if they are accessible
    if response is None:
        return False
    # Access directives in response (ensure response is a dictionary-like object)
    response_directives = getattr(response, 'directives', [])
    for directive in response_directives:
        if contains_speak_item(directive):
            return True
    print ('False')
    return False  # No SpeakItem found in the response directives