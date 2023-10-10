from uagents import Bureau
from agents.temperature_alert import agent as temperature_alert_agent

# if __name__ == "__main__":
#     bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
#     print(f"Adding temperature alert agent to Bureau: {temperature_alert_agent.address}")
#     bureau.add(temperature_alert_agent)
#     bureau.run()

import requests
import logging
from uagents import Agent, Context, Model

# Constants
OPENWEATHER_API_KEY = "bb34b4f6362247530f4b2091d0a18a9e"
DEFAULT_INTERVAL = 300.0

class TemperatureData(Model):
    temperature: float

def fetch_temperature(location, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()

        if "main" in data and "temp" in data["main"]:
            temperature = data["main"]["temp"]
            return temperature
        else:
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching temperature: {str(e)}")
        return None

def display_current_temperature(location, current_temperature):
    logging.info(f"Current temperature in {location}: {current_temperature}°C")

def temperature_alert_agent(interval, location, min_temp, max_temp, api_key):
    agent = Agent(name="TemperatureAlertAgent", seed="your_secure_agent_seed_phrase")

    @agent.on_interval(period=interval)
    async def check_temperature_alert(ctx: Context):
        try:
            current_temperature = fetch_temperature(location, api_key)

            if current_temperature is not None:
                display_current_temperature(location, current_temperature)

                if current_temperature < min_temp:
                    ctx.logger.info(f"Temperature is below {min_temp}°C. Sending alert.")
                    alert_message = f"Temperature alert: It's {current_temperature}°C, below {min_temp}°C."
                    await ctx.send(ctx.address, TemperatureData(temperature=current_temperature))

                elif current_temperature > max_temp:
                    ctx.logger.info(f"Temperature is above {max_temp}°C. Sending alert.")
                    alert_message = f"Temperature alert: It's {current_temperature}°C, above {max_temp}°C."
                    await ctx.send(ctx.address, TemperatureData(temperature=current_temperature))
        except Exception as e:
            logging.error(f"Error checking temperature alert: {str(e)}")

    @agent.on_message
    async def handle_message(ctx: Context, message: TemperatureData):
        if message.schema_digest == EXPECTED_SCHEMA_DIGEST:
            # Process the message as usual
            current_temperature = message.temperature
            display_current_temperature(location, current_temperature)
        else:
            logging.warning(f"Received a message with an unrecognized schema digest: {message.schema_digest}")

    return agent

if __name__ == "__main__":
    user_location = input("Enter your preferred location (e.g., Paris, France): ")
    min_temperature = float(input("Enter the minimum temperature threshold (e.g., 27°C): "))
    max_temperature = float(input("Enter the maximum temperature threshold (e.g., 30°C): "))


    agent = temperature_alert_agent(interval, user_location, min_temperature, max_temperature, OPENWEATHER_API_KEY)
    agent.run()
