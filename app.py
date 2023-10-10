import streamlit as st
import requests
import logging
import emails
from emails.template import JinjaTemplate as T

# Define your OpenWeather API key here
openweather_api_key = "bb34b4f6362247530f4b2091d0a18a9e"

# Function to fetch temperature from OpenWeather API
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

# Function to send email alert
def send_temperature_alert(user_email, location, current_temperature, threshold, alert_type):
    subject = T(f"Temperature {alert_type} Alert")
    html_body = T(f"<p>Temperature in {location} is {alert_type} {threshold}°C.</p>"
                  f"<p>Current temperature: {current_temperature}°C</p>")

    message = emails.html(html=html_body, subject=subject, mail_from=("Temperature Alert", "alert@mycompany.com"))

    try:
        response = message.send(to=(user_email,))
        if response.status_code == 250:
            return True  # Email sent successfully
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
    
    return False  # Email sending failed

# Streamlit app
st.title("Temperature Alert App")
user_location = st.text_input("Enter your preferred location (e.g., Paris, France):")
user_email = st.text_input("Enter your email address:")
col1, col2 = st.columns(2)
min_temp_threshold = col1.number_input("Minimum Temp (°C)", value=27)
max_temp_threshold = col2.number_input("Maximum Temp (°C)", value=30)
check_button = st.button("Check Temperature")

if check_button:
    current_temperature = fetch_temperature(user_location, openweather_api_key)

    if current_temperature is not None:
        st.write(f"Current temperature in {user_location}: {current_temperature}°C")

        if current_temperature < min_temp_threshold:
            if user_email:
                if send_temperature_alert(user_email, user_location, current_temperature, min_temp_threshold, "Low"):
                    st.success("Low temperature email alert sent successfully!")
                else:
                    st.error(f"Temperature is lower than Threshold Temperature. Sending an alert to {user_email}")
        elif current_temperature > max_temp_threshold:
            if user_email:
                if send_temperature_alert(user_email, user_location, current_temperature, max_temp_threshold, "High"):
                    st.success("High temperature email alert sent successfully!")
                else:
                    st.error(f"Temperature is Higher than Threshold Temperature. Sending an alert to {user_email}")
