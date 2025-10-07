# 6-11. Cities

# Create a dictionary with three cities as keys and their information stored in nested dictionaries
cities = {
    'new york': {
        'country': 'united states',
        'population': '8.5 million',
        'fact': 'It is home to the Statue of Liberty.'
    },
    'paris': {
        'country': 'france',
        'population': '2.1 million',
        'fact': 'The Eiffel Tower was originally meant to be temporary.'
    },
    'tokyo': {
        'country': 'japan',
        'population': '14 million',
        'fact': 'It has the busiest pedestrian crossing in the world.'
    }
}

# Loop through the dictionary and print information about each city
for city, info in cities.items():
    print(f"\nCity: {city.title()}")
    print(f" Country: {info['country'].title()}")
    print(f" Population: {info['population']}")
    print(f" Fact: {info['fact']}")