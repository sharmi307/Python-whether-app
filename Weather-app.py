
import requests

def get_weather():
    city = input("Enter city name: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    try:
        # Find the city's coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_response = requests.get(
            geo_url,
            params={"name": city, "count": 1, "language": "en"},
            timeout=15
        )
        geo_response.raise_for_status()
        places = geo_response.json().get("results", [])

        if not places:
            print("City not found. Please try another name.")
            return

        place = places[0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        # Fetch current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,is_day,"
                    "precipitation,weather_code,wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=15
        )
        weather_response.raise_for_status()
        data = weather_response.json()
        current = data["current"]

        print("\n===== LIVE WEATHER REPORT =====")
        print("City:", place["name"])
        print("Country:", place.get("country", "Unknown"))
        print("Time:", current["time"])
        print("Temperature:", current["temperature_2m"], "°C")
        print("Feels like:", current["apparent_temperature"], "°C")
        print("Humidity:", current["relative_humidity_2m"], "%")
        print("Wind speed:", current["wind_speed_10m"], "km/h")
        print("Precipitation:", current["precipitation"], "mm")
        print("Weather code:", current["weather_code"])

    except (requests.RequestException, ValueError, KeyError) as error:
        print("Unable to get weather data:", error)


if __name__ == "__main__":
    get_weather()
