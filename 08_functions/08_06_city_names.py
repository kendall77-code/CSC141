# 8-6. City Names

def city_country(city, country):
    """Return a neatly formatted city-country pair."""
    return f"{city.title()}, {country.title()}"

# Call the function with three city-country pairs
city1 = city_country("santiago", "chile")
city2 = city_country("paris", "france")
city3 = city_country("tokyo", "japan")

# Print the returned values
print(city1)
print(city2)
print(city3)