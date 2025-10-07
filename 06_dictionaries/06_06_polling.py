

# Dictionary of people who have already taken the favorite languages poll
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'python'
}

# List of people who should take the poll (some are already in the dictionary, some are not)
people_to_poll = ['jen', 'edward', 'karen', 'mike', 'sarah']

# Loop through the list of people
for person in people_to_poll:
    if person in favorite_languages:
        print(f"Thank you, {person.title()}, for responding to the poll!")
    else:
        print(f"{person.title()}, we'd like to invite you to take the favorite languages poll.")