# Exercise 10-11: Favorite Number (store)

import json

# Prompt the user for their favorite number
favorite_number = input("What is your favorite number? ")

# Save it to a file
filename = 'favorite_number.json'
with open(filename, 'w') as file_object:
    json.dump(favorite_number, file_object)

print(f"✅ Got it! I’ll remember that your favorite number is {favorite_number}.")

# Exercise 10-11: Favorite Number (read)

import json

filename = 'favorite_number.json'

try:
    with open(filename) as file_object:
        favorite_number = json.load(file_object)
except FileNotFoundError:
    print("❌ I couldn’t find your favorite number. Run the store program first.")
else:
    print(f"I know your favorite number! It’s {favorite_number}.")
