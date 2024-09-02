# Weather-api-backend
Software Engineer Intern - AI/ML Application Tech Assessment Backend using Django REST framework APIs


# WeatherPulse AI

WeatherPulse AI is a cutting-edge weather application that provides real-time weather information and forecasts with an AI-powered summary feature. This project was developed as part of the Software Engineer Intern - AI/ML Application Tech Assessment.

## Features

- **Current Weather**: Users can enter a city name to get up-to-date weather information.
- **5-Day Forecast**: Provides a detailed 5-day weather forecast for the selected location.
- **Geolocation Support**: Users can get weather information based on their current location.
- **AI-Generated Weather Summary**: Utilizing Gemini AI to generate concise and informative weather summaries.
- **Interactive UI**: Clean and responsive design with dynamic weather icons and unit conversion.

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript
- Tailwind CSS for styling
- Font Awesome for icons

### Backend
- Django (Python web framework)
- Django REST Framework for API endpoints
- OpenWeatherMap API for weather data
- Google Generative AI (Gemini) for AI-powered summaries

## Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js and npm (for Tailwind CSS)
- API keys for OpenWeatherMap and Google Generative AI (Gemini)

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weatherpulse-ai.git
   cd weatherpulse-ai
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

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install Tailwind CSS:
   ```
   npm install -D tailwindcss
   npx tailwindcss init
   ```

3. Configure Tailwind CSS by updating the `tailwind.config.js` file.

4. Build the CSS:
   ```
   npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
   ```

5. Open `index.html` in a web browser or set up a local server to serve the frontend files.

## API Endpoints

- `/api/weather/`: Get weather data for a specified city
  - Query Parameters: `city` (string)
- `/api/weather/coordinates/`: Get weather data for given coordinates
  - Query Parameters: `lat` (float), `lon` (float)
- `/api/weather/summary/`: Generate AI summary of weather data
  - Query Parameters: `city` (string), `country` (string)

## Usage

1. Open the application in a web browser.
2. Enter a city name in the search bar or click "Use My Location" for geolocation-based weather data.
3. View the current weather, 5-day forecast, and other meteorological details.
4. Click "Generate AI Summary" for an AI-powered analysis of the weather conditions.

## Contributing

Contributions to WeatherPulse AI are welcome! Please feel free to submit pull requests, create issues or spread the word.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenWeatherMap for providing weather data
- Google Generative AI (Gemini) for powering the AI summaries
- Tailwind CSS for the sleek UI design
- Font Awesome for the weather icons

---

Developed with ❤️ by [Your Name]