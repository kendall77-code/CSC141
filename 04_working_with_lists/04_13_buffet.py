# Starting buffet

# Original menu stored in a tuple
menu = ("pizza", "pasta", "salad", "soup", "breadsticks")

# Print each food the restaurant offers
print("Original menu:")
for food in menu:
    print(food)

# Try to modify one of the items (this should cause an error)
# Uncomment the line below to see Python reject the change:
# menu[0] = "burger"   # ❌ Tuples can't be changed

# The restaurant changes its menu (rewrite the tuple)
menu = ("pizza", "burger", "salad", "sushi", "fries")

# Print the revised menu
print("\nRevised menu:")
for food in menu:
    print(food)