# 6-12. Extensions - Extended Cities Program

# Extended dictionary with more keys for each city
cities = {
    'new york': {
        'country': 'united states',
        'population': '8.5 million',
        'fact': 'It is home to the Statue of Liberty.',
        'language': 'english',
        'founded': 1624
    },
    'paris': {
        'country': 'france',
        'population': '2.1 million',
        'fact': 'The Eiffel Tower was originally meant to be temporary.',
        'language': 'french',
        'founded': -52  # Roman times
    },
    'tokyo': {
        'country': 'japan',
        'population': '14 million',
        'fact': 'It has the busiest pedestrian crossing in the world.',
        'language': 'japanese',
        'founded': 1603
    },
    'rome': {
        'country': 'italy',
        'population': '2.8 million',
        'fact': 'Rome is often called “The Eternal City.”',
        'language': 'italian',
        'founded': -753  # 753 BC
    }
}

# Print a formatted header
print("=" * 50)
print(f"{'City Information Directory':^50}")
print("=" * 50)

# Sort cities alphabetically and print extended information
for city in sorted(cities.keys()):
    info = cities[city]
    print(f"\n🌆 {city.title()}")
    print(f"  Country:   {info['country'].title()}")
    print(f"  Population:{info['population']}")
    print(f"  Language:  {info['language'].title()}")
    print(f"  Founded:   {info['founded']}")
    print(f"  Fun Fact:  {info['fact']}")

print("\n" + "=" * 50)
print("End of City Directory")
print("=" * 50)