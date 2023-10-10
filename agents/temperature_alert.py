from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from messages.TemperatureAlertMessage import TemperatureAlertMessage
from messages.UAgentResponse import UAgentResponse
from messages.KeyValue import KeyValue 

TEMPERATURE_ALERT_SEED = "temperature_alert_secret_phrase" 

agent = Agent(
    name="temperature_alert",
    seed=TEMPERATURE_ALERT_SEED
)

fund_agent_if_low(agent.wallet.address())

temperature_alert_protocol = Protocol("TemperatureAlert")

@temperature_alert_protocol.on_message(model=TemperatureAlertMessage, replies=UAgentResponse)
async def handle_temperature_alert(ctx: Context, sender: str, msg: TemperatureAlertMessage):
    ctx.logger.info(f"Received temperature alert message from {sender}, session: {ctx.session}")

    location = msg.location
    min_temperature = msg.min_temperature
    max_temperature = msg.max_temperature

    ctx.logger.info(f"Location: {location}, Min Temperature: {min_temperature}, Max Temperature: {max_temperature}")

    response_message = "Temperature alert handled successfully"

    await ctx.send(
        sender,
        UAgentResponse(
            message=response_message,
            type=UAgentResponseType.FINAL_OPTIONS,
        )
    )

agent.include(temperature_alert_protocol)

