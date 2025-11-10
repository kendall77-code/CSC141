# Exercise 10-12: Favorite Number Remembered

import json

filename = 'favorite_number.json'

try:
    # Try to read the stored favorite number
    with open(filename) as file_object:
        favorite_number = json.load(file_object)
except FileNotFoundError:
    # If file doesn’t exist, prompt user for their number
    favorite_number = input("I don't know your favorite number yet. What is it? ")
    with open(filename, 'w') as file_object:
        json.dump(favorite_number, file_object)
    print(f"✅ Thanks! I’ll remember that your favorite number is {favorite_number}.")
else:
    # If file exists, print the remembered number
    print(f"🎉 I know your favorite number! It’s {favorite_number}.")
