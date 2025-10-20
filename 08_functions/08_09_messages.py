# 8-9. Messages

def show_messages(messages):
    """Print each message from the list."""
    for message in messages:
        print(message)

# List of short text messages
text_messages = [
    "Hey, how are you?",
    "Don’t forget practice at 6!",
    "I got the job!",
    "Let’s grab lunch tomorrow."
]

# Call the function
show_messages(text_messages)