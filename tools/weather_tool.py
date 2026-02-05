import requests
from typing import Dict, Any, Optional
from .base_tool import BaseTool

class WeatherTool(BaseTool):
    name = "weather_tool"
    description = "Fetches current weather for a given city name. Args: city (str)"

    def to_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city to get weather for"
                        }
                    },
                    "required": ["city"]
                }
            }
        }

    def execute(self, city: str) -> str:
        try:
            # 1. Geocode
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_res = requests.get(geo_url).json()

            if not geo_res.get("results"):
                return f"Error: Could not find coordinates for city: {city}"
            
            location = geo_res["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            city_name = location["name"]

            # 2. Weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_res = requests.get(weather_url).json()

            if "current_weather" not in weather_res:
                return f"Error: Could not fetching weather data for {city_name}"

            current = weather_res["current_weather"]
            temp = current["temperature"]
            wind = current["windspeed"]
            
            return f"Current weather in {city_name}: {temp}°C, Wind: {wind} km/h"
        except Exception as e:
            return f"Error executing WeatherTool: {str(e)}"
