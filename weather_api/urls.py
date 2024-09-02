from django.urls import path
from .views import WeatherView, GetWeatherByCoordinates, GenerateWeatherSummary

urlpatterns = [
     path('weather/', WeatherView.as_view(), name='weather_by_city'),
    path('weather/coordinates/', GetWeatherByCoordinates.as_view(), name='weather_by_coordinates'),
    path('weather/generate-weather-summary/', GenerateWeatherSummary.as_view(), name='generate_weather_summary'),
    
]
