from django.test import TestCase, RequestFactory
from django.conf import settings
from unittest.mock import patch, MagicMock
from .views import WeatherView
from .models import Weather
import json

class WeatherViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = WeatherView.as_view()
        self.api_key = 'test_api_key'
        settings.OPENWEATHERMAP_API_KEY = self.api_key

    @patch('requests.get')
    def test_get_weather_data_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'city': {'name': 'Test City', 'country': 'TC'},
            'list': [
                {
                    'main': {'temp': 20, 'temp_min': 18, 'temp_max': 22, 'humidity': 50, 'pressure': 1015},
                    'weather': [{'description': 'Clear sky'}],
                    'wind': {'speed': 5},
                    'dt_txt': '2024-03-01 12:00:00'
                }
            ] * 5  # Repeat the same data 5 times for simplicity
        }
        mock_get.return_value = mock_response

        # Make a GET request to the view
        request = self.factory.get('/weather/?city=Test City')
        response = self.view(request)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        data = json.loads(response.content)

        # Check if the processed data is correct
        self.assertEqual(data['city'], 'Test City')
        self.assertEqual(data['country'], 'TC')
        self.assertEqual(data['current']['temp_c'], 20)
        self.assertEqual(len(data['forecast']), 1)  # We only have one unique forecast in our mock data

        # Check if the weather data was saved to the database
        saved_weather = Weather.objects.first()
        self.assertIsNotNull(saved_weather)
        self.assertEqual(saved_weather.city, 'Test City')

    @patch('requests.get')
    def test_get_weather_data_failure(self, mock_get):
        # Mock a failed API response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Make a GET request to the view
        request = self.factory.get('/weather/?city=NonexistentCity')
        response = self.view(request)

        # Check if the response indicates an error
        self.assertEqual(response.status_code, 400)

        # Parse the JSON response
        data = json.loads(response.content)

        # Check if the error message is correct
        self.assertEqual(data['error'], 'Unable to fetch weather data')

    def test_default_city(self):
        # Test that the default city is New York if no city is provided
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'city': {'name': 'New York', 'country': 'US'},
                'list': [
                    {
                        'main': {'temp': 15, 'temp_min': 13, 'temp_max': 17, 'humidity': 60, 'pressure': 1010},
                        'weather': [{'description': 'Partly cloudy'}],
                        'wind': {'speed': 3},
                        'dt_txt': '2024-03-01 12:00:00'
                    }
                ] * 5
            }
            mock_get.return_value = mock_response

            request = self.factory.get('/weather/')  # No city parameter
            response = self.view(request)

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['city'], 'New York')