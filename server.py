from typing import Any
import httpx
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

OPENMETEO_API_BASE = "https://api.open-meteo.com/v1"
GEOCODING_API_BASE = "https://geocoding-api.open-meteo.com/v1"
HISTORICAL_API_BASE = "https://archive-api.open-meteo.com/v1"
USER_AGENT = "weather-app/0.1"

# Handle weather request to Open-Meteo API
async def make_openmeteo_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Open-Meteo API."""

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data from Open-Meteo API: {e}")
            return None

@mcp.tool()
async def get_coordinates_for_city(city_name: str) -> str:
    """Get the latitude and longitude for a city.
    
    Args:
        city_name (str): The name of the city.
    """

    url = f"{GEOCODING_API_BASE}/search?name={city_name}&count=1"
    data = await make_openmeteo_request(url)

    if not data or "results" not in data or not data["results"]:
        return f"Could not find coordinates for {city_name}."

    result = data["results"][0]    
    return json.dumps({
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    })

@mcp.tool()        
async def get_current_weather(latitude: float, longitude: float) -> str:
    """Get current weather for a location.
    
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
    """

    # Sample API request:
    #   https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,weather_code,surface_pressure,wind_gusts_10m
    url = f"{OPENMETEO_API_BASE}/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,weather_code,surface_pressure,wind_gusts_10m"

    data = await make_openmeteo_request(url)

    if not data:
        return "Error fetching weather data."
    
    # Provide the entire response as a string to LLM, instead of trying to format it ourselves.
    return json.dumps(data)

@mcp.tool()
async def get_daily_forecast(latitude: float, longitude: float, days: int = 7) -> str:
    """Get the daily weather forecast for a location.
    
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        days (int): Number of days to forecast (1-16). Default is 7.
    """
    
    if not 1 <= days <= 16:
        return "Error: Number of days must be between 1 and 16."

    daily_params = "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"
    url = f"{OPENMETEO_API_BASE}/forecast?latitude={latitude}&longitude={longitude}&daily={daily_params}&forecast_days={days}"

    data = await make_openmeteo_request(url)

    if not data:
        return "Error fetching weather forecast data."
        
    return json.dumps(data)

@mcp.tool()
async def get_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str) -> str:
    """Get historical weather data for a location.
    
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    """
    daily_params = "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"
    url = f"{HISTORICAL_API_BASE}/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily={daily_params}"

    data = await make_openmeteo_request(url)

    if not data:
        return "Error fetching historical weather data."
        
    return json.dumps(data)

if __name__ == "__main__":
    mcp.run(transport='stdio')
