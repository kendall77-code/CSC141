import matplotlib.pyplot as plt # type: ignore
from random import randint

class Die:
    """A class representing a single die."""
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        """Return a random value between 1 and num_sides."""
        return randint(1, self.num_sides)

# Create a D6
die = Die()

# Roll the die 1000 times and store results
results = [die.roll() for _ in range(1000)]

# Analyze the results
frequencies = [results.count(value) for value in range(1, die.num_sides + 1)]

# Visualize the results
plt.style.use('ggplot')
fig, ax = plt.subplots()
ax.bar(range(1, die.num_sides + 1), frequencies, color='skyblue', edgecolor='black')

# Label the chart
ax.set_title("Results of Rolling One D6 1,000 Times", fontsize=14)
ax.set_xlabel("Die Value", fontsize=12)
ax.set_ylabel("Frequency of Result", fontsize=12)
ax.set_xticks(range(1, die.num_sides + 1))

plt.show()

from plotly.graph_objs import Scatter, Layout # type: ignore
from plotly import offline # type: ignore
from random import choice

class RandomWalk:
    """A class to generate random walks."""
    def __init__(self, num_points=5000):
        self.num_points = num_points
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        """Calculate all the points in the walk."""
        while len(self.x_values) < self.num_points:
            x_step = choice([1, -1, 0]) * choice(range(0, 8))
            y_step = choice([1, -1, 0]) * choice(range(0, 8))

            if x_step == 0 and y_step == 0:
                continue

            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step

            self.x_values.append(x)
            self.y_values.append(y)

# Create a random walk instance and plot it
rw = RandomWalk()
rw.fill_walk()

# Prepare the data for Plotly
data = [Scatter(
    x=rw.x_values,
    y=rw.y_values,
    mode='markers',
    marker=dict(
        size=6,
        color=list(range(rw.num_points)),  # color based on position
        colorscale='Viridis',
        showscale=True
    )
)]

layout = Layout(
    title='Random Walk with Plotly',
    xaxis=dict(title='X Coordinate'),
    yaxis=dict(title='Y Coordinate'),
)

offline.plot({'data': data, 'layout': layout}, filename='random_walk_plotly.html')
