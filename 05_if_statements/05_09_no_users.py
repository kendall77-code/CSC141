# starting user

# Start with a list of usernames
usernames = ["admin", "jaden", "mia", "ethan", "sophia"]

# Check if the list is not empty
if usernames:
    for user in usernames:
        if user == "admin":
            print("Hello admin, would you like to see a status report?")
        else:
            print(f"Hello {user.title()}, thank you for logging in again.")
else:
    print("We need to find some users!")

# Remove all usernames to test the empty list case
usernames = []

# Check again after removing users
if usernames:
    for user in usernames:
        if user == "admin":
            print("Hello admin, would you like to see a status report?")
        else:
            print(f"Hello {user.title()}, thank you for logging in again.")
else:
    print("We need to find some users!")