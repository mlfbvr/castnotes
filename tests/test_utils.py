import pytest
from angler.utils import get_lat_long


def test_get_long_lat_valid():
    """Test get_long_lat with valid input."""
    location = "34.0522,-118.2437"
    longitude, latitude = get_lat_long(location)
    assert longitude == 34.0522
    assert latitude == -118.2437


def test_get_long_lat_invalid():
    """Test get_long_lat with invalid input."""
    location = "invalid_location"
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_get_long_lat_none():
    """Test get_long_lat with None input."""
    location = None
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_get_long_lat_empty_string():
    """Test get_long_lat with empty string."""
    location = ""
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_get_long_lat_missing_comma():
    """Test get_long_lat with missing comma separator."""
    location = "34.0522 -118.2437"
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_get_long_lat_too_many_values():
    """Test get_long_lat with too many comma-separated values."""
    location = "34.0522,-118.2437,10"
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_get_long_lat_with_whitespace():
    """Test get_long_lat with whitespace around values."""
    location = " 34.0522 , -118.2437 "
    longitude, latitude = get_lat_long(location)
    assert longitude == 34.0522
    assert latitude == -118.2437


def test_get_long_lat_negative_values():
    """Test get_long_lat with negative coordinates."""
    location = "-34.0522,-118.2437"
    longitude, latitude = get_lat_long(location)
    assert longitude == -34.0522
    assert latitude == -118.2437


def test_get_long_lat_zero_values():
    """Test get_long_lat with zero coordinates."""
    location = "0,0"
    longitude, latitude = get_lat_long(location)
    assert longitude == 0
    assert latitude == 0


def test_get_long_lat_single_value():
    """Test get_long_lat with only one value."""
    location = "34.0522"
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_get_long_and_lat_out_of_bounds():
    """Test get_long_lat with out-of-bounds coordinates."""
    location = "95.0,-200.0"
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_get_long_or_lat_out_of_bounds():
    """Test get_long_lat with out-of-bounds coordinates."""
    location = "34.0,-200.0"
    with pytest.raises(ValueError):
        get_lat_long(location)

    location = "-91.0,65.0"
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_get_long_lat_non_numeric():
    """Test get_long_lat with non-numeric values."""
    location = "abc,def"
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_only_one_value_with_comma():
    """Test get_long_lat with only one value but a comma."""
    location = "34.0522,"
    with pytest.raises(ValueError):
        get_lat_long(location)

    location = ",-118.2437"
    with pytest.raises(ValueError):
        get_lat_long(location)


def test_two_values_with_comma_and_extra_whitespace():
    """Test get_long_lat with two values, a comma, and extra whitespace."""
    location = " 34.0522 , -118.2437 "
    longitude, latitude = get_lat_long(location)
    assert longitude == 34.0522
    assert latitude == -118.2437
