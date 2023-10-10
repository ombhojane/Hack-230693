from enum import Enum

class UAgentResponseType(Enum):
    ERROR = "error"
    SELECT_FROM_OPTIONS = "select_from_options"
    FINAL_OPTIONS = "final_options"
