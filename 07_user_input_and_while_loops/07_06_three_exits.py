# 7-6a. Using a conditional test in the while statement

age_input = ""
while age_input != 'quit':
    age_input = input("Enter your age (or type 'quit' to stop): ")

    if age_input == 'quit':
        print("Goodbye!")
    else:
        age = int(age_input)
        if age < 3:
            print("Your ticket is free!")
        elif 3 <= age <= 12:
            print("Your ticket costs $10.")
        else:
            print("Your ticket costs $15.")

# 7-6b. Using an active variable

active = True

while active:
    age_input = input("Enter your age (or type 'quit' to stop): ")

    if age_input.lower() == 'quit':
        active = False  # Turns the flag off to end the loop
    else:
        age = int(age_input)
        if age < 3:
            print("Your ticket is free!")
        elif 3 <= age <= 12:
            print("Your ticket costs $10.")
        else:
            print("Your ticket costs $15.")