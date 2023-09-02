import requests
from twilio.rest import Client
from datetime import datetime
from config import WEATHER_API_KEY, TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, RECIPIENT_PHONE_NUMBER

def get_weather_data():
    # Get weather data from OpenWeatherMap API
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Billings"
    response = requests.get(url)
    response.raise_for_status()
    weather_data = response.json()
    return weather_data

def format_data():
    # Format data from OpenWeatherMap API
    weather_data = get_weather_data()
    city = weather_data['location']['name']
    state = weather_data['location']['region']
    temp_f = weather_data['current']['temp_f']
    feelslike_f = weather_data['current']['feelslike_f']
    humidity = weather_data['current']['humidity']
    wind_mph = weather_data['current']['wind_mph']
    wind_dir = weather_data['current']['wind_dir']
    time = weather_data['location']['localtime']
    time = datetime.strptime(time, '%Y-%m-%d %H:%M')
    time = time.strftime('%m/%d/%y %I:%M %p')
    return f"""
    {time}
    Current Weather for {city}, {state}
    Temperature: {temp_f}°F
    Feels like: {feelslike_f}°F
    Humidity: {humidity}%
    Wind: {wind_mph} mph {wind_dir}
    """

def send_weather_sms():
    # Send weather data via SMS using Twilio API
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=RECIPIENT_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        body=format_data()
    )

if __name__ == '__main__':
    send_weather_sms()
