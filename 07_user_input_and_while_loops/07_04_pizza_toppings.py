# 7-4. Pizza Toppings

print("Enter the pizza toppings you want.")
print("Type 'quit' when you are finished.\n")

while True:
    topping = input("Topping: ")

    if topping.lower() == 'quit':
        print("Okay, your pizza will be ready soon!")
        break
    else:
        print(f"I'll add {topping} to your pizza.")