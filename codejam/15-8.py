import matplotlib.pyplot as plt # type: ignore
from random import randint

class Die:
    """A class representing a single die."""

    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        """Return a random value between 1 and the number of sides."""
        return randint(1, self.num_sides)

# Create two D6 dice
die_1 = Die()
die_2 = Die()

# Roll the dice and multiply the results
results = [die_1.roll() * die_2.roll() for _ in range(1000)]

# Analyze results
max_result = die_1.num_sides * die_2.num_sides
frequencies = [results.count(value) for value in range(1, max_result + 1)]

# Plot results
x_values = list(range(1, max_result + 1))
plt.figure(figsize=(8, 5))
plt.bar(x_values, frequencies, color='salmon', edgecolor='black')
plt.title("Results of Multiplying Two D6 Dice 1,000 Times", fontsize=14)
plt.xlabel("Product of Dice", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.xticks(range(1, max_result + 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
