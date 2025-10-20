# 7-8. Deli

# List of sandwich orders
sandwich_orders = ['tuna', 'ham and cheese', 'turkey', 'pastrami', 'veggie']

# Empty list for finished sandwiches
finished_sandwiches = []

# Loop through sandwich orders
while sandwich_orders:
    current_sandwich = sandwich_orders.pop(0)  # take the first order
    print(f"I made your {current_sandwich} sandwich.")
    finished_sandwiches.append(current_sandwich)

# Display all finished sandwiches
print("\nAll sandwiches have been made:")
for sandwich in finished_sandwiches:
    print(f"- {sandwich.title()} sandwich")