# starting username

# List of current usernames
current_users = ["admin", "Jaden", "Mia", "Ethan", "Sophia"]

# List of new usernames (some duplicates, case-insensitive)
new_users = ["mia", "Noah", "ETHAN", "Liam", "olivia"]

# Create a lowercase version of current_users for case-insensitive comparison
current_users_lower = [user.lower() for user in current_users]

# Check each new username
for new_user in new_users:
    if new_user.lower() in current_users_lower:
        print(f"Sorry, the username '{new_user}' is already taken. Please enter a new one.")
    else:
        print(f"The username '{new_user}' is available.")
        