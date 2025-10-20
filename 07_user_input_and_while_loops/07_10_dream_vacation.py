# 7-10. Dream Vacation

# Dictionary to store poll responses
responses = {}

polling_active = True

while polling_active:
    # Ask for the user's name and dream vacation
    name = input("\nWhat is your name? ")
    vacation = input("If you could visit one place in the world, where would you go? ")

    # Store the response in the dictionary
    responses[name] = vacation

    # Ask if another person would like to respond
    repeat = input("Would you like to let someone else respond? (yes/no): ")
    if repeat.lower() == 'no':
        polling_active = False

# Polling is complete
print("\n--- Dream Vacation Poll Results ---")
for name, vacation in responses.items():
    print(f"{name.title()} would like to visit {vacation.title()}.")