import matplotlib.pyplot as plt # type: ignore
from random import choice

class RandomWalkModified:
    """A modified random walk class with custom directions and distances."""

    def __init__(self, num_points=5000):
        self.num_points = num_points
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        """Generate the points in the random walk with modified rules."""
        while len(self.x_values) < self.num_points:
            # Modify directions and distances for experimentation
            x_direction = choice([1])          # only positive x movement
            x_distance = choice(range(0, 9))   # longer possible steps (0–8)
            x_step = x_direction * x_distance

            y_direction = choice([1, -1])      # still move both up and down
            y_distance = choice(range(0, 9))   # longer possible steps (0–8)
            y_step = y_direction * y_distance

            if x_step == 0 and y_step == 0:
                continue

            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step

            self.x_values.append(x)
            self.y_values.append(y)

# Create a modified random walk and plot the results
rw_mod = RandomWalkModified(5000)
rw_mod.fill_walk()

plt.figure(figsize=(8, 6))
plt.plot(rw_mod.x_values, rw_mod.y_values, linewidth=1)
plt.title("Modified Random Walk (Longer Distances, One-Sided X Direction)", fontsize=14)
plt.xlabel("X Position", fontsize=12)
plt.ylabel("Y Position", fontsize=12)
plt.grid(True)
plt.show()
