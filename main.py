from uagents import Bureau
from agents.temperature_alert import agent as temperature_alert_agent

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    print(f"Adding temperature alert agent to Bureau: {temperature_alert_agent.address}")
    bureau.add(temperature_alert_agent)
    bureau.run()
