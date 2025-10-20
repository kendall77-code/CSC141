# 8-4. Large Shirts

def make_shirt(size="large", message="I love Python"):
    """Display information about the shirt being made, with default values."""
    print(f"\nMaking a {size} shirt with the message: '{message}'.")

# Make a large shirt with the default message
make_shirt()

# Make a medium shirt with the default message
make_shirt(size="medium")

# Make a custom-sized shirt with a different message
make_shirt(size="small", message="Keep Coding!")