# -*- coding: utf-8 -*-

# HowTo skill: A simple skill that shows how to use python's
# gettext module for localization, for multiple locales.

import logging
import gettext
import requests
import json
from dotenv import load_dotenv
import os

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from ask_sdk_model.dialog import (
    ElicitSlotDirective, DelegateDirective)

from alexa import data, util


sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

# Access the API key from the environment variables
api_key = os.getenv('VOICEFLOW_API_KEY')

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        locale = handler_input.request_envelope.request.locale
        item = util.get_random_item(locale)
        url = "https://general-runtime.voiceflow.com/state/user/userEXAMPLE/interact?logs=off"
        payload = {
            "action": {
                "type": "launch",
            },
            "config": {
                "tts": False,
                "stripSSML": True,
                "stopAll": True,
                "excludeTypes": ["block", "debug", "flow"]
            }
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": api_key
        }
        
        response1 = requests.post(url, json=payload, headers=headers)
        data_json1 = response1.text
        data1 = json.loads(data_json1)
        
        for item in data1:  # Corrected variable name from 'data' to 'data1'
            # Check if the item is a dictionary and contains the keys 'type' and 'payload'
            if isinstance(item, dict) and 'type' in item and 'payload' in item:
                # Check if the payload is a dictionary and contains the key 'message'
                if isinstance(item['payload'], dict) and 'message' in item['payload']:
                    # Extract and print the message
                    message1 = item['payload']['message']

        speak_output = message1
        response_builder = handler_input.response_builder
        return response_builder.speak(speak_output).ask(speak_output).response


class InfoIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In InfoIntentHandler")
        url = "https://general-runtime.voiceflow.com/state/user/userEXAMPLE/interact?logs=off"
        catch_all_slot_value = handler_input.request_envelope.request.intent.slots["CatchAll"].value
        payload = {
            "action": {
                "type": "text",
                "payload": catch_all_slot_value
            },
            "config": {
                "tts": False,
                "stripSSML": True,
                "stopAll": True,
                "excludeTypes": ["block", "debug", "flow"]
            }
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": api_key
        }
        
        response1 = requests.post(url, json=payload, headers=headers)
        
        data_json1 = response1.text
        data1 = json.loads(data_json1)
        
        for item in data1:  # Corrected variable name from 'data' to 'data1'
            # Check if the item is a dictionary and contains the keys 'type' and 'payload'
            if isinstance(item, dict) and 'type' in item and 'payload' in item:
                # Check if the payload is a dictionary and contains the key 'message'
                if isinstance(item['payload'], dict) and 'message' in item['payload']:
                    # Extract and print the message
                    message1 = item['payload']['message']

        speak_output = message1
        print (response1.json())
        response_builder = handler_input.response_builder

        return (
            response_builder
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .speak(speak_output).ask("")
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        locale = handler_input.request_envelope.request.locale
        item = util.get_random_item(locale)

        speech = _(data.HELP_MESSAGE).format(item)

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        session_attributes = handler_input.attributes_manager.session_attributes
        handler_input.response_builder.speak(
            session_attributes['speech']).ask(
            session_attributes['reprompt'])
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler for Cancel and Stop Intents."""
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        speech = _(data.STOP_MESSAGE).format(_(data.SKILL_NAME))
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        locale = handler_input.request_envelope.request.locale
        item = util.get_random_item(locale)

        help_message = _(data.HELP_MESSAGE).format(item)
        help_reprompt = _(data.HELP_REPROMPT).format(item)
        speech = _(data.FALLBACK_MESSAGE).format(
            _(data.SKILL_NAME)) + help_message
        reprompt = _(data.FALLBACK_MESSAGE).format(
            _(data.SKILL_NAME)) + help_reprompt

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for SessionEndedRequest."""
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Global exception handler."""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = _("Sorry, I can't understand the command. Please say again!!")
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class CacheSpeechForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the output speech and reprompt to session attributes,
    for repeat intent.
    """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["speech"] = response.output_speech
        session_attr["reprompt"] = response.reprompt


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(InfoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

#sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_response_interceptor(CacheSpeechForRepeatInterceptor())

lambda_handler = sb.lambda_handler()
