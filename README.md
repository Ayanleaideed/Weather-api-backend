# WeatherPulse AI Backend

## Overview
This is the backend component of WeatherPulse AI, a cutting-edge weather application that provides real-time weather information and forecasts with an AI-powered summary feature. This project was developed as part of the Software Engineer Intern - AI/ML Application Tech Assessment.

## Quick Links
- **Video Demo**: [Watch the demo video](https://youtube.com)
- **Live Backend REST API**: [https://weather-api-backend-eta.vercel.app/api/weather/](https://weather-api-backend-eta.vercel.app/api/weather/)
- **Frontend Application**: [https://weather-front-end-sigma.vercel.app/](https://weather-front-end-sigma.vercel.app/)
- **Frontend Github repo**: https://github.com/Ayanleaideed/Weather-Front-end

## Features
- **Weather Data Retrieval**: Fetches current weather and forecast data from OpenWeatherMap API.
- **Geolocation Support**: Provides weather information based on latitude and longitude coordinates.
- **AI-Generated Weather Summary**: Utilizes Google Generative AI (Gemini) to create concise and informative weather summaries.
- **Data Caching**: Implements in-memory storage for efficient data retrieval and AI summary generation.

## Technology Stack
- Django (Python web framework)
- Django REST Framework for API endpoints
- OpenWeatherMap API for weather data
- Google Generative AI (Gemini) for AI-powered summaries

## Technology Stack Front-end
- HTML5
- CSS3 (with Tailwind CSS for styling)
- JavaScript
- Font Awesome for icons
- jQuery for AJAX requests


## Setup and Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weather-api-backend.git
   cd weather-api-backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the Django development server:
   ```
   python manage.py runserver
   ```

## API Endpoints
- `/api/weather/`: Get weather data for a specified city
  - Method: GET
  - Query Parameters: `city` (string)

- `/api/weather/coordinates/`: Get weather data for given coordinates
  - Method: GET
  - Query Parameters: `lat` (float), `lon` (float)

- `/api/weather/generate-weather-summary/`: Generate AI summary of weather data
  - Method: GET
  - Query Parameters: `city` (string)

## Usage
The backend is designed to be used in conjunction with the WeatherPulse AI frontend. It provides the necessary API endpoints for fetching weather data and generating AI summaries.

## Contributing
Contributions to WeatherPulse AI Backend are welcome! Please feel free to submit pull requests, create issues or spread the word.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- OpenWeatherMap for providing weather data
- Google Generative AI (Gemini) for powering the AI summaries
- Django and Django REST Framework for the robust backend architecture

---
Developed with ❤️ by Ayanle Aideed
