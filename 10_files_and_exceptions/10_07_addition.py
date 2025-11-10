# Exercise 10-7: Addition Calculator

print("Welcome to the Addition Calculator!")
print("Enter two numbers, and I’ll add them for you.")
print("Type 'quit' at any time to exit.\n")

while True:
    first_number = input("Enter the first number: ")
    if first_number.lower() == 'quit':
        print("\nGoodbye! 👋")
        break

    second_number = input("Enter the second number: ")
    if second_number.lower() == 'quit':
        print("\nGoodbye! 👋")
        break

    try:
        # Try converting inputs to integers
        result = int(first_number) + int(second_number)
    except ValueError:
        # If conversion fails, show a friendly message and continue
        print("❌ Oops! Please enter valid numbers.\n")
        continue
    else:
        # Print result if inputs were valid
        print(f"✅ The sum of {first_number} and {second_number} is {result}.\n")
