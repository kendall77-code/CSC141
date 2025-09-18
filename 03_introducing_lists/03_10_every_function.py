cities = ["Egpyt", "Tokyo", "Rome", "London", "Paris"]

print("Original list of cities:")
print(cities)

print("\nFirst city in the list:", cities[0])
print("Last city in the list:", cities[-1])

cities.append("Rome")          
print("\nList after adding a city with append():")
print(cities)

cities.insert(2, "Sydney")     
print("\nList after inserting a city at position 2 with insert():")
print(cities)

removed_city = cities.pop()   
print(f"\nRemoved city with pop(): {removed_city}")
print("List after pop():")
print(cities)

cities.remove("Tokyo")        
print("\nList after removing 'Tokyo' with remove():")
print(cities)

print("\nList in alphabetical order with sorted():")
print(sorted(cities))         

print("\nList still in its current order:")
print(cities)                  

cities.sort()                
print("\nList after using sort():")
print(cities)

cities.sort(reverse=True)      
print("\nList after using sort(reverse=True):")
print(cities)

cities.reverse()
print("\nList after using reverse():")
print(cities)

print(f"\nNumber of cities in the list: {len(cities)}")
