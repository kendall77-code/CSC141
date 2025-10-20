# 8-3. T-Shirt

def make_shirt(size, message):
    """Display information about the shirt being made."""
    print(f"\nMaking a {size} shirt with the message: '{message}'.")

# Call the function using positional arguments
make_shirt("large", "Dream Big!")

# Call the function using keyword arguments
make_shirt(size="medium", message="Code Like a Pro")