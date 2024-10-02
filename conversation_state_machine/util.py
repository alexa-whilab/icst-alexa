import json
import os

from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective)


def load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    current_dir = os.path.dirname(__file__)
    with open(current_dir + file_path) as f:
        return json.load(f)

def render_document(response_builder, token, document, datasources=None):
    response_builder.add_directive(
    RenderDocumentDirective(
        token = token,
        document = load_apl_document(document),
        datasources = datasources))
    return response_builder

def execute_command(response_builder,token, commands):
    response_builder.add_directive(
    ExecuteCommandsDirective(
        token = token,
        commands = commands))
    return response_builder

def animate_display_change(disappear_element_id=None, new_text_id = None, new_text=None, appear_element_id=None):
    command = [{
        "type": "Sequential",
        "commands": [
        ]
    }
    ]
    if disappear_element_id:
        command[0]["commands"].append({
            "type": "AnimateItem",
            "easing": "ease-in-out",
            "componentId": disappear_element_id,
            "duration": 700,
            "value": [
                {
                    "property": "opacity",
                    "to": 0
                }
            ]
        })
    # If new_text is provided, add the SetValue command to update the text
    if new_text_id and new_text:
        command[0]["commands"].append({
            "type": "SetValue",
            "componentId": new_text_id,
            "property": "text",
            "value": new_text
        })

    # Add the animation for the appearing element
    if appear_element_id:
        command[0]["commands"].append({
            "type": "AnimateItem",
            "easing": "ease-in-out",
            "componentId": appear_element_id,
            "duration": 700,
            "value": [
                {
                    "property": "opacity",
                    "from": 0,
                    "to": 1
                }
            ]
        }) 
    
    return command


def render_document_speakitem(response_builder, token, document, response_text=""):
    datasources = {
        "LambdaData": {
            "type": "object",
            "properties": {
                "text": response_text,
                "text_ssml": "<speak>{}</speak>".format(response_text)
            },
            "transformers": [
            {
                "inputPath": "text_ssml",
                "transformer": "ssmlToSpeech",
                "outputName": "text_speech"
            }
            ]
        }
    }
    response_builder.add_directive(
    RenderDocumentDirective(
        token = token,
        document = load_apl_document(document),
        datasources = datasources))
    return response_builder
