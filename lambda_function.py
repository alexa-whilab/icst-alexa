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
from alexa.state_machine import ConversationManager


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
        response_builder = handler_input.response_builder
        conversation_manager = ConversationManager()
        user_utterance = util.get_user_utterance(handler_input)
        session_data = util.get_session_data(handler_input)
        print (session_data, user_utterance)
        result = conversation_manager.initate_conversation(user_utterance, session_data)

        
        response_text = result['speech']
        session_data['dialogue_state'] = result['state']
        return response_builder.speak(response_text).ask(response_text).response


class InfoIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In InfoIntentHandler")
        response_builder = handler_input.response_builder
        conversation_manager = ConversationManager()
        user_utterance = util.get_user_utterance(handler_input)
        session_data = util.get_session_data(handler_input)
        print (session_data, user_utterance)
        result = conversation_manager.process_request(user_utterance, session_data)
        response_text = result['speech']
        session_data['dialogue_state'] = result['state']

        return (
            response_builder
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .speak(response_text).ask("")
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
