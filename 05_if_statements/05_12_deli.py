# starting deli

# ✅ Good variable naming (lowercase_with_underscores)
favorite_color = "blue"
age = 17
username = "Admin"

# ✅ Proper spacing around operators and after commas
if favorite_color == "blue":
    print("Blue is your favorite color!")

# ✅ Lowercasing before comparison (case-insensitive check)
if username.lower() == "admin":
    print("Hello admin, would you like to see a status report?")

# ✅ Clear, properly indented if-elif-else chain
if age < 13:
    print("You're a kid.")
elif age < 20:
    print("You're a teenager.")
else:
    print("You're an adult.")

# ✅ Membership checks with clear formatting
fruits = ["apple", "banana", "mango"]
if "banana" in fruits:
    print("You really like bananas!")

if "orange" not in fruits:
    print("You don't like oranges or they aren't in the list.")