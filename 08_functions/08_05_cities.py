# 8-5. Cities

def describe_city(city, country="Iceland"):
    """Display a simple sentence describing a city and its country."""
    print(f"{city.title()} is in {country.title()}.")

# Call the function for three different cities
describe_city("reykjavik")          # uses default country
describe_city("akureyri")           # uses default country
describe_city("tokyo", "japan")     # overrides the default