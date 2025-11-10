# Exercise 10-6: Addition

print("Welcome to the addition calculator!")
print("Enter two numbers, and I’ll add them for you.")
print("Type 'quit' at any time to exit.\n")

while True:
    first_number = input("Enter the first number: ")
    if first_number.lower() == 'quit':
        break

    second_number = input("Enter the second number: ")
    if second_number.lower() == 'quit':
        break

    try:
        # Try to convert both inputs to integers
        result = int(first_number) + int(second_number)
    except ValueError:
        # Handle cases where input isn’t numeric
        print("❌ Oops! Please enter valid numbers.\n")
    else:
        # Only runs if no exception occurs
        print(f"✅ The sum of {first_number} and {second_number} is {result}.\n")
