// --------------------------------------------
// AgriCare - Weather Module (Client Side)
// --------------------------------------------

const WEATHER_API_KEY = "4ecea42e195e9c6ea17050db3869e16b";
const WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather";

// DOM Elements
const tempEl = document.getElementById("temp");
const humidityEl = document.getElementById("humidity");
const windEl = document.getElementById("wind");
const descEl = document.getElementById("weather-description");
const iconEl = document.getElementById("weather-icon");

// Update UI safely
function updateWeatherUI(data) {
    if (!data || !data.main) {
        descEl.textContent = "Weather unavailable";
        return;
    }

    tempEl.textContent = data.main.temp.toFixed(1);
    humidityEl.textContent = data.main.humidity;
    windEl.textContent = data.wind.speed;
    descEl.textContent = data.weather[0].description.toUpperCase();
    iconEl.src = `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;
}

// Fetch weather using coordinates
function fetchWeather(lat, lon) {
    fetch(`${WEATHER_URL}?lat=${lat}&lon=${lon}&units=metric&appid=${WEATHER_API_KEY}`)
        .then(response => response.json())
        .then(data => updateWeatherUI(data))
        .catch(() => {
            descEl.textContent = "Unable to fetch weather";
        });
}

// Get user location
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
        position => {
            fetchWeather(
                position.coords.latitude,
                position.coords.longitude
            );
        },
        () => {
            descEl.textContent = "Location permission denied";
        }
    );
} else {
    descEl.textContent = "Geolocation not supported";
}
