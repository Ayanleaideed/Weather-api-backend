from django.http import JsonResponse
from django.views import View
import requests
from django.conf import settings
from .models import Weather
import google.generativeai as genai
from django.utils import timezone

# In-memory storage for weather data
weather_data_store = {}

class WeatherView(View):
    def get(self, request):
        city = request.GET.get('city', 'New York')
        api_key = settings.OPENWEATHERMAP_API_KEY
        
        # Fetch weather data from OpenWeatherMap
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the data
            processed_data = {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'current': {
                    'temp_c': data['list'][0]['main']['temp'],
                    'description': data['list'][0]['weather'][0]['description'],
                    'wind_speed': data['list'][0]['wind']['speed'],
                    'humidity': data['list'][0]['main']['humidity'],
                    'pressure': data['list'][0]['main']['pressure']
                },
                'forecast': [
                    {
                        'date': item['dt_txt'].split()[0],
                        'temp_min': item['main']['temp_min'],
                        'temp_max': item['main']['temp_max'],
                        'description': item['weather'][0]['description']
                    } for item in data['list'][::8]  # Get data for every 24 hours
                ]
            }
            # Store the data in the in-memory dictionary for  ai summary generation 
            weather_data_store['latest'] = processed_data
            
            # Retrieve the last saved weather data for the city
            last_saved_weather = Weather.objects.filter(city=processed_data['city']).order_by('-id').first()
            
            # Check if the last saved city matches the current one and the data is the same
            if not last_saved_weather or (
                last_saved_weather.country != processed_data['country'] or
                last_saved_weather.temperature != processed_data['current']['temp_c'] or
                last_saved_weather.description != processed_data['current']['description'] or
                last_saved_weather.humidity != processed_data['current']['humidity'] or
                last_saved_weather.wind_speed != processed_data['current']['wind_speed'] or
                last_saved_weather.pressure != processed_data['current']['pressure'] or
                last_saved_weather.forecast != processed_data['forecast']
            ):
                # Save the new weather data if it is different
                Weather.objects.create(
                    city=processed_data['city'],
                    country=processed_data['country'],
                    temperature=processed_data['current']['temp_c'],
                    description=processed_data['current']['description'],
                    humidity=processed_data['current']['humidity'],
                    wind_speed=processed_data['current']['wind_speed'],
                    pressure=processed_data['current']['pressure'],
                    forecast=processed_data['forecast'],
                    timestamp=timezone.now()
                )
            return JsonResponse(processed_data)
        else:
            return JsonResponse({'error': 'Unable to fetch weather data'}, status=400)



class GetWeatherByCoordinates(View):
    def get(self, request):
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')
        api_key = settings.OPENWEATHERMAP_API_KEY
        
        if not latitude or not longitude:
            return JsonResponse({'error': 'Latitude and Longitude are required parameters.'}, status=400)
        
        # Fetch weather data from OpenWeatherMap by coordinates
        url = f'http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the data
            processed_data = {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'current': {
                    'temp_c': data['list'][0]['main']['temp'],
                    'description': data['list'][0]['weather'][0]['description'],
                    'wind_speed': data['list'][0]['wind']['speed'],
                    'humidity': data['list'][0]['main']['humidity'],
                    'pressure': data['list'][0]['main']['pressure'], 
                    "uv": 1
                },
                
                'forecast': [
                    {
                        'date': item['dt_txt'].split()[0],
                        'temp_min': item['main']['temp_min'],
                        'temp_max': item['main']['temp_max'],
                        'description': item['weather'][0]['description']
                    } for item in data['list'][::8]  # Get data for every 24 hours
                ]
            }
            # Store the data in the in-memory dictionary
            weather_data_store['latest'] = processed_data
            
             # Retrieve the last saved weather data for the city
            last_saved_weather = Weather.objects.filter(city=processed_data['city']).order_by('-id').first()
            
            # Check if the last saved city matches the current one and the data is the same
            if not last_saved_weather or (
                last_saved_weather.country != processed_data['country'] or
                last_saved_weather.temperature != processed_data['current']['temp_c'] or
                last_saved_weather.description != processed_data['current']['description'] or
                last_saved_weather.humidity != processed_data['current']['humidity'] or
                last_saved_weather.wind_speed != processed_data['current']['wind_speed'] or
                last_saved_weather.pressure != processed_data['current']['pressure'] or
                last_saved_weather.forecast != processed_data['forecast']
            ):
                # Save the new weather data if it is different
                Weather.objects.create(
                    city=processed_data['city'],
                    country=processed_data['country'],
                    temperature=processed_data['current']['temp_c'],
                    description=processed_data['current']['description'],
                    humidity=processed_data['current']['humidity'],
                    wind_speed=processed_data['current']['wind_speed'],
                    pressure=processed_data['current']['pressure'],
                    forecast=processed_data['forecast'],
                )
            return JsonResponse(processed_data)
        else:
            return JsonResponse({'error': 'Unable to fetch weather data'}, status=400)




class GenerateWeatherSummary(View):
    def get(self, request):
        # Retrieve the last weather data from the in-memory store
        last_weather_data = weather_data_store.get('latest', None)
        
        if not last_weather_data:
            return JsonResponse({'error': 'No weather data available.'}, status=400)
        
        # Prepare the prompt for the AI
        prompt = self.prepare_prompt(last_weather_data)
        
        # Generate the summary using Gemini
        try:
            summary = self.generate_ai_summary(prompt)
            # Ensure the summary is clean and formatted
            formatted_summary = self.format_summary(summary)
            return JsonResponse({'summary': formatted_summary})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def prepare_prompt(self, weather_data):
        current = weather_data['current']
        forecast = weather_data['forecast']
        
        prompt = f"Generate a concise weather summary for {weather_data['city']}, {weather_data['country']}. "
        prompt += f"Current temperature: {current['temp_c']}°C. "
        prompt += f"Description: {current['description']}. "
        prompt += f"Wind speed: {current['wind_speed']} m/s. "
        prompt += f"Humidity: {current['humidity']}%. "
        prompt += f"Pressure: {current['pressure']} hPa. "
        prompt += "Provide a brief 5-day forecast summary:\n"
        
        for day in forecast:
            prompt += f"{day['date']}: Min {day['temp_min']}°C, Max {day['temp_max']}°C, {day['description']}\n You should be up in correct English. He's a friendly and make sure you do not add a weird syntax like markdown. This should be normal sentence."
        
        prompt += "\nSummarize any notable changes in the weather and provide brief recommendations on what to wear."
        
        return prompt

    def generate_ai_summary(self, prompt):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    
    def format_summary(self, summary):
        # Replace new lines with spaces and limit the text length
        cleaned_summary = summary.replace('\n', ' ')
        # Ensure the text is concise and easy to read
        return cleaned_summary[:4000]  # Limit to a reasonable length 
