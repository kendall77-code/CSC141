# Starting loops

# Original list of pizzas
pizzas = ["pepperoni", "margherita", "bbq chicken"]

# Friend's pizza list (copy)
friend_pizzas = pizzas[:]

# Add different pizzas to each list
pizzas.append("buffalo chicken")
friend_pizzas.append("veggie")

# Print each list using for loops
print("My favorite pizzas are:")
for pizza in pizzas:
    print(pizza)

print("\nMy friend's favorite pizzas are:")
for pizza in friend_pizzas:
    print(pizza)
    