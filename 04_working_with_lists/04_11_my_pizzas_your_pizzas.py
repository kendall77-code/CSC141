# Starting pizza

# Original list of pizzas
pizzas = ["pepperoni", "margherita", "bbq chicken"]

# Make a copy of the list
friend_pizzas = pizzas[:]

# Add a new pizza to the original list
pizzas.append("buffalo chicken")

# Add a different pizza to the friend's list
friend_pizzas.append("veggie")

# Prove they are two separate lists
print("My favorite pizzas are:")
for pizza in pizzas:
    print(pizza)

print("\nMy friend's favorite pizzas are:")
for pizza in friend_pizzas:
    print(pizza)
