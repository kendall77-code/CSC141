# Exercise 10-5: Guest Book

print("Welcome to the guest book!")
print("Enter 'quit' anytime to exit.\n")

# Open the file in append mode so new guests are added to the end
with open('guest_book.txt', 'a') as file_object:
    while True:
        name = input("What is your name? ")

        if name.lower() == 'quit':
            print("\nGoodbye! Guest book updated.")
            break
        else:
            # Write each guest name on a new line
            file_object.write(name + "\n")
            print(f"Welcome, {name}! Your name has been added to the guest book.\n")
