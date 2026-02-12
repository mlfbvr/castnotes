def get_lat_long(location_string):
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
