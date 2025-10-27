import matplotlib.pyplot as plt # type: ignore
from random import choice

class RandomWalkRefactored:
    """A random walk class with refactored step logic."""

    def __init__(self, num_points=5000):
        self.num_points = num_points
        self.x_values = [0]
        self.y_values = [0]

    def get_step(self):
        """Determine the direction and distance for a step."""
        direction = choice([1, -1])
        distance = choice([0, 1, 2, 3, 4])
        return direction * distance

    def fill_walk(self):
        """Generate all points in the walk using the refactored method."""
        while len(self.x_values) < self.num_points:
            x_step = self.get_step()
            y_step = self.get_step()

            # Reject moves that go nowhere
            if x_step == 0 and y_step == 0:
                continue

            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step

            self.x_values.append(x)
            self.y_values.append(y)

# Create a refactored random walk and plot it
rw_ref = RandomWalkRefactored(5000)
rw_ref.fill_walk()

plt.figure(figsize=(8, 6))
plt.plot(rw_ref.x_values, rw_ref.y_values, linewidth=1)
plt.title("Refactored Random Walk (Using get_step Method)", fontsize=14)
plt.xlabel("X Position", fontsize=12)
plt.ylabel("Y Position", fontsize=12)
plt.grid(True)
plt.show()
