# Exercise 10-4: Guest

# Prompt the user for their name
name = input("What is your name? ")

# Write the name to guest.txt
with open('guest.txt', 'w') as file_object:
    file_object.write(name)

print(f"Welcome, {name}! Your name has been added to guest.txt.")
