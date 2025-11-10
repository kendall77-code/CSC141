def city_country(city, country, population=None):
    """Return a neatly formatted city, country string with optional population."""
    if population:
        full_name = f"{city.title()}, {country.title()} - population {population}"
    else:
        full_name = f"{city.title()}, {country.title()}"
    return full_name

from city_functions import city_country # type: ignore

def test_city_country():
    """Test city_country() with just city and country."""
    formatted_name = city_country('santiago', 'chile')
    assert formatted_name == 'Santiago, Chile'

def test_city_country_population():
    """Test city_country() with city, country, and population."""
    formatted_name = city_country('santiago', 'chile', population=5000000)
    assert formatted_name == 'Santiago, Chile - population 5000000'
