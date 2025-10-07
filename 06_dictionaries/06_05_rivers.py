# 6-5. Rivers
# Create a dictionary with rivers as keys and countries as values
rivers = {
    'nile': 'egypt',
    'amazon': 'brazil',
    'yangtze': 'china'
}

# Loop to print a sentence about each river
for river, country in rivers.items():
    print(f"The {river.title()} runs through {country.title()}.")

print()  # blank line for readability

# Loop to print the name of each river
print("Rivers included in the dictionary:")
for river in rivers.keys():
    print(f"- {river.title()}")

print()  # blank line for readability

# Loop to print the name of each country
print("Countries included in the dictionary:")
for country in rivers.values():
    print(f"- {country.title()}")