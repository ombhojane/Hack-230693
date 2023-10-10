from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Json


class UAgentResponseType(Enum):
    ERROR = "error"
    SELECT_FROM_OPTIONS = "select_from_options"
    FINAL_OPTIONS = "final_options"


class KeyValue(BaseModel):
    key: str
    value: str

    class Config:
        json_encoders = {
            Json: lambda v: v,  # Use a custom encoder for JSON serialization
        }


class UAgentResponse(BaseModel):
    type: UAgentResponseType
    agent_address: Optional[str]
    message: Optional[str]
    options: Optional[List[KeyValue]]
    request_id: Optional[str]
