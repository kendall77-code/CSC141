# 6-10. Favorite Numbers (Multiple Numbers)

# Create a dictionary where each person has a list of favorite numbers
favorite_numbers = {
    'alice': [7, 12, 19],
    'bob': [3, 8],
    'charlie': [5],
    'diana': [10, 22, 33],
    'ethan': [2, 4, 6, 8]
}

# Loop through the dictionary and print each person's favorite numbers
for name, numbers in favorite_numbers.items():
    print(f"\n{name.title()}'s favorite numbers are:")
    for number in numbers:
        print(f" - {number}")