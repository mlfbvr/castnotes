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

    if latitude is None or longitude is None:
        raise ValueError("Could not parse latitude and longitude from location string")

    # Raise value error if latitude or longitude are not valid floats
    if not isinstance(latitude, float) or not isinstance(longitude, float):
        raise ValueError("Latitude and longitude must be valid float numbers")

    return latitude, longitude
