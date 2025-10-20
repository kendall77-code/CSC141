# 7-5. Movie Tickets

print("Welcome to the movie theater!")
print("Enter your age to find out your ticket price.")
print("Type 'quit' when you are finished.\n")

while True:
    age_input = input("Please enter your age: ")

    if age_input.lower() == 'quit':
        print("Thank you for visiting! Enjoy the show!")
        break

    age = int(age_input)

    if age < 3:
        print("Your ticket is free!")
    elif 3 <= age <= 12:
        print("Your ticket costs $10.")
    else:
        print("Your ticket costs $15.")