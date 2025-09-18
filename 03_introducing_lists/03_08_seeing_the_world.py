places = ["Egpyt", "Tokyo", "Rome", "London", "Paris"]
print("Original list:")
print(places)

print("\nList in alphabetical order:")
print(sorted(places))

print("\nList still in original order:")
print(places)

print("\nList in reverse-alphabetical order:")
print(sorted(places, reverse=True))

print("\nList still in original order again:")
print(places)

places.reverse()
print("\nList after using reverse():")
print(places)

places.reverse()
print("\nList after using reverse() again:")
print(places)

places.sort()
print("\nList after using sort() (alphabetical):")
print(places)

places.sort(reverse=True)
print("\nList after using sort() (reverse-alphabetical):")
print(places)