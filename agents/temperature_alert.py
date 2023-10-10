from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from messages.TemperatureAlertMessage import TemperatureAlertMessage
from messages.UAgentResponse import UAgentResponse
from messages.KeyValue import KeyValue  # Import the KeyValue class correctly

TEMPERATURE_ALERT_SEED = "temperature_alert_secret_phrase"  # Adjust the seed as needed

# Create the TemperatureAlert Agent
agent = Agent(
    name="temperature_alert",
    seed=TEMPERATURE_ALERT_SEED
)

# Fund the agent if the balance is low
fund_agent_if_low(agent.wallet.address())

# Define the TemperatureAlert Protocol
temperature_alert_protocol = Protocol("TemperatureAlert")

# Define the handler for TemperatureAlert messages
@temperature_alert_protocol.on_message(model=TemperatureAlertMessage, replies=UAgentResponse)
async def handle_temperature_alert(ctx: Context, sender: str, msg: TemperatureAlertMessage):
    ctx.logger.info(f"Received temperature alert message from {sender}, session: {ctx.session}")

    # Extract data from the message
    location = msg.location
    min_temperature = msg.min_temperature
    max_temperature = msg.max_temperature

    # Here, you can implement logic to fetch real-time temperature data for the specified location
    # Compare the temperature with the thresholds (min_temperature and max_temperature)
    # Send an alert/notification to the user if the temperature goes beyond the thresholds

    # For demonstration purposes, let's print the extracted data
    ctx.logger.info(f"Location: {location}, Min Temperature: {min_temperature}, Max Temperature: {max_temperature}")

    # You can implement temperature checking and notification logic here

    # Create a response message (for demonstration)
    response_message = "Temperature alert handled successfully"

    # Send a response to the user
    await ctx.send(
        sender,
        UAgentResponse(
            message=response_message,
            type=UAgentResponseType.FINAL_OPTIONS,
        )
    )

# Include the TemperatureAlert Protocol in the agent
agent.include(temperature_alert_protocol)

# You can add more protocols, configurations, or logic to this agent as needed
