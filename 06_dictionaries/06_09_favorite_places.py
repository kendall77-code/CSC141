# 6-9. Favorite Places

# Create a dictionary with people's names as keys and lists of their favorite places as values
favorite_places = {
    'kendall': ['new york', 'miami', 'los angeles'],
    'alice': ['paris', 'rome'],
    'marcus': ['tokyo', 'seoul', 'bangkok']
}

# Loop through the dictionary and print each person's favorite places
for name, places in favorite_places.items():
    print(f"\n{name.title()}'s favorite places are:")
    for place in places:
        print(f" - {place.title()}")