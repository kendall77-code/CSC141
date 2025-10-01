# Starting slice

# Base list: first 10 cubes
cubes = [number ** 3 for number in range(1, 11)]

# Print the first three items in the list
print("The first three items in the list are:")
print(cubes[:3])

# Print three items from the middle of the list
print("\nThree items from the middle of the list are:")
middle_index = len(cubes) // 2  # middle point
print(cubes[middle_index - 1:middle_index + 2])

# Print the last three items in the list
print("\nThe last three items in the list are:")
print(cubes[-3:])
