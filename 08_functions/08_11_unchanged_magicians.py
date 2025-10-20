# 8-11. Archived Messages

def send_messages(messages, sent_messages):
    """Print each message and move it to sent_messages."""
    while messages:
        current_message = messages.pop(0)
        print(f"Sending message: {current_message}")
        sent_messages.append(current_message)

# Original list of messages
text_messages = [
    "Hey, how are you?",
    "Don’t forget practice at 6!",
    "I got the job!",
    "Let’s grab lunch tomorrow."
]

# Empty list for sent messages
sent_messages = []

# Call the function using a COPY of the list
send_messages(text_messages[:], sent_messages)

# Show both lists after sending
print("\nFinal Lists:")
print(f"Original messages (unchanged): {text_messages}")
print(f"Sent messages: {sent_messages}")