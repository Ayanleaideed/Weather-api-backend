import requests
from datetime import datetime

def get_weather_forecast(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses
    data = response.json()
    
    forecast = []
    for item in data['list'][:5]:  # Get forecast for next 5 time steps
        forecast_item = {
            'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': item['main']['temp'],
            'weather': item['weather'][0]['description']
        }
        forecast.append(forecast_item)
    import json
    with open("weather.json", "w") as f:
        json.dump(data, f)
    
    return forecast

# Example usage
api_key = '945ed49e5932c29ac840d19cc1bf1a0c'
lat = 46.8772  # Latitude for West Fargo, ND
lon = -96.7898  # Longitude for West Fargo, ND

try:
    forecast = get_weather_forecast(api_key, lat, lon)
    for day in forecast:
        print(f"Date: {day['date']}, Temperature: {day['temperature']}°C, Weather: {day['weather']}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")