# 6-7. People

# Create three dictionaries representing different people
person1 = {
    'first_name': 'Kendall',
    'last_name': 'Hazzard',
    'age': 17,
    'city': 'Newark'
}

person2 = {
    'first_name': 'Alice',
    'last_name': 'Johnson',
    'age': 22,
    'city': 'Chicago'
}

person3 = {
    'first_name': 'Marcus',
    'last_name': 'Lee',
    'age': 19,
    'city': 'Houston'
}

# Store all three dictionaries in a list
people = [person1, person2, person3]

# Loop through the list and print information about each person
for person in people:
    print(f"Name: {person['first_name']} {person['last_name']}")
    print(f"Age: {person['age']}")
    print(f"City: {person['city']}\n")