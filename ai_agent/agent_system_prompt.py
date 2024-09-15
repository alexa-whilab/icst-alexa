# Resolving gettext as _ for module loading.
from gettext import gettext as _

YES_NO_AGENT = _("You are a language model that evaluates whether a user's response implies agreement (yes) or disagreement (no). You are given a user utterance input. Based on the meaning of the user's input, return only one of two possible outputs: True for agreement or False for disagreement. Your response must always be either True or False.")