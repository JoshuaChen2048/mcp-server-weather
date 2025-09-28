# MCP Weather Server

This is my Agentic AI practice project for MCP server.

This project implements a simple weather server that uses the `mcp` library to expose a single tool, `get_current_weather`, which fetches weather data from the [Open-Meteo API](https://open-meteo.com/).

## Features

*   Provides current weather data for a given latitude and longitude.
*   Uses the `mcp` library to create a tool server.
*   Asynchronously fetches data from the Open-Meteo API using `httpx`.

## Requirements

*   Python 3.13+
*   `httpx>=0.28.1`
*   `mcp[cli]>=1.15.0`

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/JoshuaChen2048/mcp-server-weather.git
    cd mcp-server-weather
    ```

2.  **Install dependencies:**

    It is recommended to use a virtual environment.

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt 
    ```

## Usage

To run the server, execute the following command:

```bash
mcp run server.py
```

The server will start and listen for requests on stdio.

## MCP Client Configuration

To use this tool with an MCP client, you need to configure the client to run the server.

### Claude Desktop Example

Here is an example configuration for Claude Desktop's `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/Users/JoshuaC/.pyenv/shims/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/Users/JoshuaC/Documents/projects/mcp-server-weather/server.py"
      ]
    }
  }
}
```

**Note:** The paths in this example are specific to a particular user's environment. You will need to adjust the `command` and the path to `server.py` to match your own system's configuration.

## API

### `get_coordinates_for_city(city_name: str) -> str`

Retrieves the latitude and longitude for a given city name.

**Arguments:**

*   `city_name` (str): The name of the city.

**Returns:**

*   `str`: A JSON string containing the latitude and longitude, or an error message if the city could not be found.

### `get_current_weather(latitude: float, longitude: float) -> str`

Retrieves the current weather for a specified location.

**Arguments:**

*   `latitude` (float): The latitude of the location.
*   `longitude` (float): The longitude of the location.

**Returns:**

*   `str`: A JSON string containing the current weather data from the Open-Meteo API, or an error message if the data could not be fetched.

### `get_daily_forecast(latitude: float, longitude: float, days: int = 7) -> str`

Retrieves the daily weather forecast for a specified location.

**Arguments:**

*   `latitude` (float): The latitude of the location.
*   `longitude` (float): The longitude of the location.
*   `days` (int, optional): The number of days to forecast, between 1 and 16. Defaults to 7.

**Returns:**

*   `str`: A JSON string containing the daily weather forecast data from the Open-Meteo API, or an error message if the data could not be fetched.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.