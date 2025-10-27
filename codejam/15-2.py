import matplotlib.pyplot as plt # type: ignore

# Generate the first 5,000 cubic numbers
x_values = list(range(1, 5001))
y_values = [x**3 for x in x_values]

# Create a scatter plot with a colormap
plt.figure(figsize=(8, 6))
plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.viridis, s=5)
plt.title("Cubes Colored by Value", fontsize=14)
plt.xlabel("Value", fontsize=12)
plt.ylabel("Cube of Value", fontsize=12)
plt.colorbar(label="Cube Value")
plt.grid(True)
plt.show()
