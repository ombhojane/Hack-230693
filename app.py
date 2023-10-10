import streamlit as st
import requests
import logging
import emails
from emails.template import JinjaTemplate as T
import openai
import os


# Define your OpenWeather API key here
openweather_api_key = st.secrets("OPENWEATHER_API_KEY")

# List of weather conditions and icons
weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Drizzle": "🌧️",
    "Rain": "🌧️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Smoke": "🌫️",
    "Haze": "🌫️",
    "Dust": "🌫️",
    "Fog": "🌫️",
    "Sand": "🌫️",
    "Ash": "🌫️",
    "Squall": "🌫️",
    "Tornado": "🌪️"
}

def fetch_temperature(location, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 

        data = response.json()

        if "main" in data and "temp" in data["main"]:
            temperature = data["main"]["temp"]
            return temperature
        else:
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching temperature: {str(e)}")
        return None

def send_temperature_alert(user_email, location, current_temperature, threshold, alert_type):
    subject = T(f"Temperature {alert_type} Alert")
    html_body = T(f"<p>Temperature in {location} is {alert_type} {threshold}°C.</p>"
                  f"<p>Current temperature: {current_temperature}°C</p>")

    message = emails.html(html=html_body, subject=subject, mail_from=("Temperature Alert", "alert@mycompany.com"))

    try:
        response = message.send(to=(user_email,))
        if response.status_code == 250:
            return True 
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
    
    return False  

def fetch_weather_condition(location, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  

        data = response.json()

        if "weather" in data and len(data["weather"]) > 0:
            weather_condition = data["weather"][0]["main"]
            return weather_condition
        else:
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather condition: {str(e)}")
        return None

def generate_suggestions(location, current_temperature, min_temp_threshold, max_temp_threshold, weather_condition):
    
    openai.api_key = st.secrets["openai_api_key"]

    if min_temp_threshold <= current_temperature <= max_temp_threshold:
        prompt = f"Provide suggestions for someone in {location} where it's {current_temperature}°C and {weather_condition}."
    elif current_temperature < min_temp_threshold:
        prompt = f"Provide suggestions for someone in {location} where it's {current_temperature}°C and {weather_condition}. " \
                 f"Recommend suitable clothing and precautions for cold weather."
    else:
        prompt = f"Provide suggestions for someone in {location} where it's {current_temperature}°C and {weather_condition}. " \
                 f"Recommend suitable clothing and precautions for hot weather."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=600,  
        n=1,              
        stop=None,        
        temperature=0.7,  
    )

    suggestions = response.choices[0].text
    return suggestions


def main():
    st.title("Fetch Alerts : Personalized Weather Suggestions App")
    user_location = st.text_input("Enter your preferred location (e.g., Paris, France):")
    user_email = st.text_input("Enter your email address:")
    col1, col2 = st.columns(2)
    min_temp_threshold = col1.number_input("Minimum Temp (°C)", value=27)
    max_temp_threshold = col2.number_input("Maximum Temp (°C)", value=30)
    check_button = st.button("Check Temperature and Weather")

    if check_button:
        weather_condition = fetch_weather_condition(user_location, openweather_api_key)

        if weather_condition is not None:
            st.header(f"Results of {user_location} {weather_icons[weather_condition]}")
            current_temperature = fetch_temperature(user_location, openweather_api_key)

            if current_temperature is not None:
                st.write(f"Current temperature: {current_temperature}°C")

                if current_temperature < min_temp_threshold:
                    if user_email:
                        if send_temperature_alert(user_email, user_location, current_temperature, min_temp_threshold, "Low"):
                            st.success("Low temperature email alert sent successfully!")
                        else:
                            st.error(f"Failed to send a low temperature alert to {user_email}")
                elif current_temperature > max_temp_threshold:
                    if user_email:
                        if send_temperature_alert(user_email, user_location, current_temperature, max_temp_threshold, "High"):
                            st.success("High temperature email alert sent successfully!")
                        else:
                            st.error(f"Failed to send a high temperature alert to {user_email}")

             
                suggestions = generate_suggestions(user_location, current_temperature, min_temp_threshold, max_temp_threshold, weather_condition)
                st.subheader("Personalized Suggestions:")
                st.write(suggestions)

if __name__ == "__main__":
    main()
