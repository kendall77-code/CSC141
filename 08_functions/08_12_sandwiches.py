# 8-12. Sandwiches

def make_sandwich(*items):
    """Summarize the sandwich being made."""
    print("\nMaking a sandwich with the following items:")
    for item in items:
        print(f"- {item.title()}")
    print("Your sandwich is ready!")

# Call the function three times with different numbers of ingredients
make_sandwich('turkey', 'lettuce', 'tomato')
make_sandwich('ham', 'cheese')
make_sandwich('chicken', 'bacon', 'lettuce', 'mayo')