# city_functions.py

def city_country(city, country):
    """Return a string formatted like 'City, Country'."""
    formatted_location = f"{city.title()}, {country.title()}"
    return formatted_location

# test_cities.py

from city_functions import city_country # type: ignore

def test_city_country():
    """Test that city_country() correctly formats city and country names."""
    formatted = city_country('santiago', 'chile')
    assert formatted == 'Santiago, Chile'
