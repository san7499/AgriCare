import requests

# 🔑 Replace with your own OpenWeatherMap API key
API_KEY = "4ecea42e195e9c6ea17050db3869e16b"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_by_city(city="Pune"):
    """
    Get weather using city name
    """
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if response.status_code != 200:
            return {
                "error": "Unable to fetch weather data"
            }

        return {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"]
        }

    except Exception as e:
        return {
            "error": "Weather service not available"
        }


def get_weather_by_coordinates(lat, lon):
    """
    Get weather using latitude & longitude
    """
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if response.status_code != 200:
            return {
                "error": "Unable to fetch weather data"
            }

        return {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"]
        }

    except Exception:
        return {
            "error": "Weather service not available"
        }
