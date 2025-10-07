# 6-8. Pets

# Create several dictionaries representing different pets
pet1 = {
    'animal': 'dog',
    'owner': 'Kendall'
}

pet2 = {
    'animal': 'cat',
    'owner': 'Alice'
}

pet3 = {
    'animal': 'parrot',
    'owner': 'Marcus'
}

pet4 = {
    'animal': 'hamster',
    'owner': 'Diana'
}

# Store the dictionaries in a list
pets = [pet1, pet2, pet3, pet4]

# Loop through the list and print information about each pet
for pet in pets:
    print(f"Animal: {pet['animal'].title()}")
    print(f"Owner: {pet['owner'].title()}")
    print()  # blank line for readability