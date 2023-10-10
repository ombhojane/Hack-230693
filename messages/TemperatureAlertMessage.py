from uagents import Model
from pydantic import Field

class TemperatureAlertMessage(Model):
    location: str = Field(description="Location for which temperature is monitored")
    min_temperature: float = Field(description="Minimum temperature threshold")
    max_temperature: float = Field(description="Maximum temperature threshold")
