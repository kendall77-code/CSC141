# Exercise 10-13: User Dictionary

import json

filename = 'user_info.json'

try:
    # Try to read existing user data
    with open(filename) as file_object:
        user_data = json.load(file_object)
except FileNotFoundError:
    # If file doesn't exist, collect user information
    print("👋 Hello! Let's get to know you better.\n")
    name = input("What is your name? ")
    age = input("How old are you? ")
    color = input("What’s your favorite color? ")

    # Store the information in a dictionary
    user_data = {
        'name': name,
        'age': age,
        'favorite_color': color
    }

    # Save dictionary to file
    with open(filename, 'w') as file_object:
        json.dump(user_data, file_object)

    print(f"\n✅ Thanks, {name}! I’ll remember your information.")
else:
    # If data exists, display what we remember
    print("🎉 Welcome back! Here’s what I remember about you:\n")
    print(f"Name: {user_data['name']}")
    print(f"Age: {user_data['age']}")
    print(f"Favorite Color: {user_data['favorite_color']}")
