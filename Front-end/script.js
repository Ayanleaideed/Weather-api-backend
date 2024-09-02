// DOM elements
const weatherInfo = document.getElementById('weatherInfo');
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const locationBtn = document.getElementById('locationBtn');
const aiSummaryBtn = document.getElementById('aiSummaryBtn');
const aiSummary = document.getElementById('aiSummary');
const unitToggle = document.getElementById('unitToggle');
const themeToggle = document.getElementById('themeToggle');

// Global variables
let isFahrenheit = true;
let lastFetchedData = null;
let currentCity = '';
const summaryCache = new Map();

// Event listeners
searchBtn.addEventListener('click', () => fetchWeather(cityInput.value, 'search'));
cityInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        fetchWeather(cityInput.value.trim() || 'New York', 'search');
    }
});
locationBtn.addEventListener('click', useGeolocation);
aiSummaryBtn.addEventListener('click', generateAISummary);
unitToggle.addEventListener('click', toggleTemperatureUnit);
themeToggle.addEventListener('click', toggleTheme);

// Theme functions
function initializeTheme() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    document.documentElement.classList.toggle('dark', isDarkMode);
    updateThemeToggleButton(isDarkMode);
}

function updateThemeToggleButton(isDark) {
    const moonIcon = themeToggle.querySelector('.fa-moon');
    const sunIcon = themeToggle.querySelector('.fa-sun');
    moonIcon.classList.toggle('hidden', isDark);
    sunIcon.classList.toggle('hidden', !isDark);
}

function toggleTheme() {
    const isDarkMode = document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', isDarkMode);
    updateThemeToggleButton(isDarkMode);
}

// Geolocation functions
function useGeolocation() {
    hideError();
    if (navigator.geolocation) {
        showLoader();
        navigator.geolocation.getCurrentPosition(
            position => fetchWeatherByCoordinates(position.coords.latitude, position.coords.longitude),
            handleGeolocationError,
            { timeout: 10000, maximumAge: 0, enableHighAccuracy: true }
        );
    } else {
        showError("Geolocation is not supported by your browser. Using default location of New York.");
        fetchWeather('New York', 'fallback');
    }
}

function handleGeolocationError(error) {
    const errorMessages = {
        1: "Location access was denied.",
        2: "Location information is unavailable.",
        3: "The request to get user location timed out.",
        0: "An unknown error occurred while trying to get your location."
    };
    showError(errorMessages[error.code] + " Using default location of New York.");
    fetchWeather('New York', 'fallback');
}

// Weather fetching functions
async function fetchWeatherByCoordinates(lat, lon) {
    try {
        showLoader();
        const response = await fetch(`http://127.0.0.1:8000/api/weather/coordinates/?lat=${lat}&lon=${lon}`);
        const data = await response.json();
        
        if (response.status !== 200) {
            throw new Error(data.error || 'Unable to fetch weather data.');
        }
        
        if (data.city !== currentCity) {
            summaryCache.delete(currentCity);
        }
        
        lastFetchedData = data;
        currentCity = data.city;
        displayWeather(data);
        hideError();
    } catch (error) {
        console.error('Error fetching weather data:', error);
        showError("Failed to fetch weather data for your location. Using default location of New York.");
        await fetchWeather('New York', 'fallback');
    } finally {
        hideLoader();
    }
}

async function fetchWeather(city, source) {
    try {
        showLoader();
        console.log('Fetching weather data...');
        const response = await fetch('https://weather-api-backend-eta.vercel.app/api/weather/', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
        });
        
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Received data:', data);

        if (city !== currentCity) {
            summaryCache.delete(currentCity);
        }
        
        lastFetchedData = data;
        currentCity = data.city;
        displayWeather(data);
        if (source !== 'fallback') hideError();
    } catch (error) {
        console.error('Detailed error in fetchWeather:', error);
        showError(`An error occurred while fetching weather data. Error: ${error.message}`);
    } finally {
        hideLoader();
    }
}



// Weather display functions
function displayWeather(data) {
    weatherInfo.classList.remove('hidden');
    const current = data.current;
    const location = { name: data.city, country: data.country };

    document.getElementById('cityName').textContent = `${location.name}, ${location.country}`;
    document.getElementById('currentDate').textContent = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    updateTemperature('temperature', current.temp_c);
    document.getElementById('weatherDescription').textContent = current.description;
    document.getElementById('weatherIcon').className = `fas ${getWeatherIcon(current.description)} text-6xl`;
    document.getElementById('wind').textContent = `${current.wind_speed.toFixed(1)} mph`;
    document.getElementById('humidity').textContent = `${current.humidity.toFixed(0)}%`;
    document.getElementById('pressure').textContent = `${current.pressure.toFixed(2)} hPa`;
    document.getElementById('uvIndex').textContent = '3'; // UV Index not provided by our API

    updateForecast(data.forecast);
}

function updateForecast(forecastData) {
    const forecastContainer = document.getElementById('forecast');
    forecastContainer.innerHTML = forecastData.map(day => {
        const date = new Date(day.date);
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
        const tempHigh = convertTemperature(day.temp_max);
        const tempLow = convertTemperature(day.temp_min);
        const tempAvg = (tempHigh + tempLow) / 2;
        return `
            <div class="bg-white bg-opacity-20 dark:bg-gray-700 rounded-lg p-4 text-center transition-colors duration-300">
                <p class="font-bold">${dayName}</p>
                <p class="text-sm">${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</p>
                <i class="fas ${getWeatherIcon(day.description)} text-3xl my-2"></i>
                <p class="font-bold">${tempAvg.toFixed(1)}°${isFahrenheit ? 'F' : 'C'}</p>
                <p class="text-sm">H: ${tempHigh.toFixed(1)}° L: ${tempLow.toFixed(1)}°</p>
                <p class="text-xs mt-2">${day.description}</p>
            </div>
        `;
    }).join('');
}

function updateTemperature(elementId, temperatureCelsius) {
    const temperature = convertTemperature(temperatureCelsius);
    document.getElementById(elementId).textContent = `${temperature.toFixed(1)}°${isFahrenheit ? 'F' : 'C'}`;
}

function toggleTemperatureUnit() {
    isFahrenheit = !isFahrenheit;
    unitToggle.classList.toggle('celsius', !isFahrenheit);
    if (lastFetchedData) {
        displayWeather(lastFetchedData);
    }
}

function convertTemperature(celsius) {
    return isFahrenheit ? (celsius * 9 / 5) + 32 : celsius;
}

function getWeatherIcon(description) {
    const icons = {
        'sun': 'fa-sun text-yellow-400',
        'clear': 'fa-sun text-yellow-400',
        'cloud': 'fa-cloud text-gray-400',
        'rain': 'fa-cloud-rain text-blue-400',
        'shower': 'fa-cloud-showers-heavy text-blue-500',
        'snow': 'fa-snowflake text-blue-200'
    };
    return Object.keys(icons).find(key => description.toLowerCase().includes(key)) 
           ? icons[Object.keys(icons).find(key => description.toLowerCase().includes(key))] 
           : 'fa-cloud text-gray-400';
}

// AI Summary functions
async function generateAISummary() {
    if (!currentCity) {
        showError('Please search for a city first.');
        return;
    }

    if (summaryCache.has(currentCity)) {
        displayCachedSummary();
        return;
    }

    showLoaderAi();
    aiSummaryBtn.disabled = true;

    try {
        const aiSummaryElement = document.getElementById('aiSummary');
        aiSummaryElement.classList.add('hidden');

        // Simulate a delay (3 seconds)
        await new Promise(resolve => setTimeout(resolve, 3000));

        const response = await fetch(`http://127.0.0.1:8000/api/weather/generate-weather-summary/?city=${encodeURIComponent(currentCity)}`);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        summaryCache.set(currentCity, data.summary);
        displayCachedSummary();
    } catch (error) {
        console.error('Error fetching weather summary:', error);
        showError('Failed to retrieve weather summary.');
    } finally {
        hideLoaderAi();
        aiSummaryBtn.disabled = false;
    }
}

function displayCachedSummary() {
    const aiSummaryElement = document.getElementById('aiSummary');
    const summaryParagraph = aiSummaryElement.querySelector('p');
    summaryParagraph.innerHTML = summaryCache.get(currentCity);
    aiSummaryElement.classList.remove('hidden');
}

// Utility functions
function showLoader() {
    document.getElementById('loader-overlay').classList.remove('hidden');
}

function hideLoader() {
    document.getElementById('loader-overlay').classList.add('hidden');
}

function showLoaderAi() {
    document.getElementById('loader-ai').classList.remove('hidden');
}

function hideLoaderAi() {
    document.getElementById('loader-ai').classList.add('hidden');
}

function showError(message) {
    const errorComponent = document.getElementById('error-component');
    document.getElementById('error-message').textContent = message;
    errorComponent.classList.remove('hidden');
}

function hideError() {
    document.getElementById('error-component').classList.add('hidden');
}

function dismissError() {
    hideError();
}

// Initialize the theme on page load
initializeTheme();

// Use geolocation on load, fallback to New York
window.onload = function() {
    useGeolocation();
    initializeTheme();
};