# 7-9. No Pastrami

# List of sandwich orders (with 'pastrami' appearing multiple times)
sandwich_orders = ['tuna', 'pastrami', 'ham and cheese', 'pastrami', 'turkey', 'veggie', 'pastrami']

# Empty list for finished sandwiches
finished_sandwiches = []

# Announce that the deli has run out of pastrami
print("The deli has run out of pastrami!\n")

# Remove all occurrences of 'pastrami'
while 'pastrami' in sandwich_orders:
    sandwich_orders.remove('pastrami')

# Make the remaining sandwiches
while sandwich_orders:
    current_sandwich = sandwich_orders.pop(0)
    print(f"I made your {current_sandwich} sandwich.")
    finished_sandwiches.append(current_sandwich)

# Display all finished sandwiches
print("\nAll sandwiches have been made (no pastrami!):")
for sandwich in finished_sandwiches:
    print(f"- {sandwich.title()} sandwich")