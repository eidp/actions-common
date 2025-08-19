from .generate_workflow_docs import generate_workflow_docs
from .generate_workflow_list import generate_workflow_list
from .generate_action_docs import generate_action_docs
from .generate_action_list import generate_action_list

def generate_workflows():
    """
    Generate all documentation for workflows and actions.
    This function is intended to be run as a script.
    """
    generate_workflow_docs()
    generate_workflow_list()

def generate_actions():
    """
    Generate all documentation for actions.
    This function is intended to be run as a script.
    """
    generate_action_docs()
    generate_action_list()