def get_lat_long(location_string: str):
    """Extract latitude and longitude from a comma-separated location string. Raises ValueError for invalid inputs."""
    # Raise ValueError for invalid inputs
    if not location_string:
        raise ValueError("Location string is empty or None")

    if "," not in location_string:
        raise ValueError("Location string must contain a comma separator")

    latitude, longitude = map(float, location_string.split(","))

    if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
        raise ValueError("Latitude or longitude out of bounds")

    return latitude, longitude


def get_weather_for_location(location_string: str):
    """Fetch weather data for a given location string using OpenWeatherMap API. Returns None if fetching fails."""
    import requests
    import os

    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        raise ValueError("OpenWeatherMap API key not set in environment variables")

    try:
        latitude, longitude = get_lat_long(location_string)
    except ValueError as e:
        raise ValueError(f"Error parsing location string: {e}")

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise requests.RequestException(f"Error fetching weather data: {e}")

    return response.json()


def get_name_for_location(location_string: str):
    """Fetch the name of the location for a given location string using OpenWeatherMap API. Returns None if fetching fails."""
    import requests
    import os

    api_key = os.getenv("LOCIQ_API_KEY")
    if not api_key:
        raise ValueError("OpenWeatherMap API key not set in environment variables")

    try:
        latitude, longitude = get_lat_long(location_string)
    except ValueError as e:
        raise ValueError(f"Error parsing location string: {e}")

    url = "https://us1.locationiq.com/v1/reverse"  # Or https://eu1.locationiq.com/v1/reverse for EU server
    params = {
        "lat": latitude,
        "lon": longitude,
        "key": api_key,
        "format": "json",
        "addressdetails": 1,
    }

    response = requests.get(url, params=params)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise requests.RequestException(f"Error fetching weather data: {e}")

    data = response.json()
    return data.get("name", "Unknown Location")
