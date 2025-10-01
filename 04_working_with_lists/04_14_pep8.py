# Starting pep8

def main():
    """Create a list of numbers from 1 to 1,000,000 and print the min, max, and sum."""
numbers = list(range(1, 1000001))

print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
print("Sum:", sum(numbers))

if __name__ == "main":
    main()

def print_cubes(n=10):
    """Print the first n cubes using a list comprehension."""
    cubes = [number ** 3 for number in range(1, n + 1)]
    for cube in cubes:
        print(cube)


if __name__ == "__main__":
    print_cubes()

def show_pizza_preferences():
    """Show me and my friend's favorite pizzas."""
    my_pizzas = ["Pepperoni","Sausage","Bacon"]
    friend_pizzas = my_pizzas[:]

    my_pizzas.append("Buffalo")
    friend_pizzas.append("Veggie")

    print("My favorite pizzas are:")
    for pizza in my_pizzas:
        print(pizza)

    print("My friend's favorite pizzas are:")
    for pizza in friend_pizzas:
        print(pizza)


if __name__ == "__main__":
    show_pizza_preferences()
