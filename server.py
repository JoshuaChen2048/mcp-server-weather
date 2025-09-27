from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

OPENMETEO_API_BASE = "https://api.open-meteo.com/v1/"
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
        
if __name__ == "__main__":
    mcp.run(transport='stdio')
