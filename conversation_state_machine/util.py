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

def render_document(response_builder, document, datasources=None):
    response_builder.add_directive(
    RenderDocumentDirective(
        token = document,
        document = load_apl_document(document),
        datasources = datasources))
    return response_builder

def execute_command(response_builder, command, datasources=None):
    response_builder.add_directive(
    ExecuteCommandsDirective(
        token = command,
        command = load_apl_document(command),
        datasources = datasources))
    return response_builder