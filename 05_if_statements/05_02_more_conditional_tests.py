# starting more

# --- String equality and inequality ---
fruit = 'apple'
print("Is fruit == 'apple'? I predict True.")
print(fruit == 'apple')

print("\nIs fruit != 'banana'? I predict True.")
print(fruit != 'banana')

print("\nIs fruit == 'orange'? I predict False.")
print(fruit == 'orange')

# --- Tests using lower() ---
name = 'KENDALL'
print("\nIs name.lower() == 'kendall'? I predict True.")
print(name.lower() == 'kendall')

print("\nIs name.lower() == 'john'? I predict False.")
print(name.lower() == 'john')

# --- Numerical tests ---
age = 18
print("\nIs age == 18? I predict True.")
print(age == 18)

print("\nIs age != 21? I predict True.")
print(age != 21)

print("\nIs age > 16? I predict True.")
print(age > 16)

print("\nIs age < 16? I predict False.")
print(age < 16)

print("\nIs age >= 18? I predict True.")
print(age >= 18)

print("\nIs age <= 17? I predict False.")
print(age <= 17)

# --- Tests using 'and' and 'or' ---
height = 175
weight = 70

print("\nIs height > 170 and weight < 80? I predict True.")
print(height > 170 and weight < 80)

print("\nIs height < 170 and weight < 80? I predict False.")
print(height < 170 and weight < 80)

print("\nIs height > 180 or weight < 80? I predict True.")
print(height > 180 or weight < 80)

print("\nIs height < 160 or weight > 100? I predict False.")
print(height < 160 or weight > 100)

# --- Test whether an item is in a list ---
colors = ['red', 'blue', 'green']

print("\nIs 'red' in colors? I predict True.")
print('red' in colors)

print("\nIs 'purple' in colors? I predict False.")
print('purple' in colors)

# --- Test whether an item is not in a list ---
print("\nIs 'yellow' not in colors? I predict True.")
print('yellow' not in colors)

print("\nIs 'blue' not in colors? I predict False.")
print('blue' not in colors)

